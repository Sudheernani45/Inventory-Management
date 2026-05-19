"""
manager_routes.py — routes for the Manager role.

Manager permissions:
  Products  : view, edit, delete  (cannot add new products)
  Sites     : view only           (cannot edit/delete)
  Inventory : view (site-scoped)
  Sales     : view (site-scoped)
  POs       : create, approve, cancel
  SOs       : create, cancel
  Adjustments: apply stock adjustments
  Alerts    : view stockout / low-stock alerts
"""
from flask import Blueprint, render_template, session, jsonify, request
from models.db import db
from models.user import User
from models.managers import Manager
from models.records import Site, Inventory, Sale, Product, Logistics, Promotion, SeasonalPlan, Category, Subcategory, Supplier, PurchaseOrder, SalesOrder, AuditLog, StockLevel, StockMovement, Customer, States, SalesReturn, PurchaseReturn
from routes.auth_routes import login_required, role_required, handle_errors
from utils.audit import log_action
from sqlalchemy import func
import random, string, json
from datetime import date

manager_bp = Blueprint('manager', __name__)

PER_PAGE = 20


# ── Helpers ───────────────────────────────────────────────
def _manager_site_id():
    """Return the site_id assigned to the currently logged-in manager."""
    mgr = Manager.query.filter_by(user_id=session['user_id']).first()
    return mgr.site_id if mgr else None


def _random_id(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))




# ═══════════════════════════════════════════════════════════
#  PAGE ROUTES
# ═══════════════════════════════════════════════════════════

@manager_bp.route('/dashboard')
@login_required
@role_required('manager')
@handle_errors
def dashboard():
    return render_template('manager/dashboard.html')


@manager_bp.route('/products')
@login_required
@role_required('manager')
@handle_errors
def products():
    return render_template('manager/products.html')


@manager_bp.route('/inventory')
@login_required
@role_required('manager')
@handle_errors
def inventory():
    return render_template('manager/inventory.html')


@manager_bp.route('/adjustments')
@login_required
@role_required('manager')
@handle_errors
def adjustments():
    return render_template('manager/adjustments.html')


@manager_bp.route('/purchase-orders')
@login_required
@role_required('manager')
@handle_errors
def purchase_orders():
    return render_template('manager/purchase_orders.html')


@manager_bp.route('/sales-orders')
@login_required
@role_required('manager')
@handle_errors
def sales_orders():
    return render_template('manager/sales_orders.html')


@manager_bp.route('/sales')
@login_required
@role_required('manager')
@handle_errors
def sales():
    return render_template('manager/sales.html')


@manager_bp.route('/alerts')
@login_required
@role_required('manager')
@handle_errors
def alerts():
    return render_template('manager/alerts.html')


@manager_bp.route('/site')
@login_required
@role_required('manager')
@handle_errors
def site_view():
    return render_template('manager/site.html')


@manager_bp.route('/sites')
@login_required
@role_required('manager')
@handle_errors
def sites():
    return render_template('manager/sites.html')


# ═══════════════════════════════════════════════════════════
#  JSON API
# ═══════════════════════════════════════════════════════════

# ── Dashboard stats ───────────────────────────────────────
@manager_bp.route('/api/stats')
@login_required
@role_required('manager')
@handle_errors
def manager_stats():
    site_id   = _manager_site_id()
    site_name = None
    if site_id:
        s = Site.query.filter_by(site_id=site_id).first()
        site_name = s.site_name if s else site_id

    q_rev  = db.session.query(func.sum(Sale.revenue))
    q_units= db.session.query(func.sum(Sale.units_sold))
    q_stock= Inventory.query.filter_by(stockout_flag='Yes')
    if site_id:
        q_rev   = q_rev.filter(Sale.site_id == site_id)
        q_units = q_units.filter(Sale.site_id == site_id)
        q_stock = q_stock.filter(Inventory.site_id == site_id)

    return jsonify({
        'total_revenue':  float(q_rev.scalar()   or 0),
        'units_sold':     int(q_units.scalar()    or 0),
        'stockout_count': q_stock.count(),
        'product_count':  Product.query.count(),
        'site_id':        site_id,
        'site_name':      site_name,
    })


# ── Alert count (for sidebar badge) ──────────────────────
@manager_bp.route('/api/alert-count')
@login_required
@role_required('manager')
@handle_errors
def alert_count():
    site_id = _manager_site_id()
    q = Inventory.query.filter_by(stockout_flag='Yes')
    if site_id:
        q = q.filter(Inventory.site_id == site_id)
    return jsonify({'count': q.count()})


# ── Alerts list ───────────────────────────────────────────
@manager_bp.route('/api/alerts')
@login_required
@role_required('manager')
@handle_errors
def get_alerts():
    site_id = _manager_site_id()
    level   = request.args.get('level', '').strip()
    alerts  = []

    # Stockout alerts (critical)
    q_so = (db.session.query(Inventory, Product)
            .join(Product, Inventory.product_id == Product.product_id, isouter=True)
            .filter(Inventory.stockout_flag == 'Yes'))
    if site_id:
        q_so = q_so.filter(Inventory.site_id == site_id)
    for inv, p in q_so.limit(50).all():
        alerts.append({
            'level':      'critical',
            'title':      f'Stockout: {p.product_name if p else inv.product_id}',
            'message':    f'Product has zero ending inventory at site {inv.site_id}.',
            'product_id': inv.product_id,
        })

    # Low stock alerts (ending_inventory > 0 but <= 10 → warning)
    q_low = (db.session.query(Inventory, Product)
             .join(Product, Inventory.product_id == Product.product_id, isouter=True)
             .filter(Inventory.stockout_flag != 'Yes')
             .filter(Inventory.ending_inventory <= 10)
             .filter(Inventory.ending_inventory > 0))
    if site_id:
        q_low = q_low.filter(Inventory.site_id == site_id)
    for inv, p in q_low.limit(50).all():
        alerts.append({
            'level':      'warning',
            'title':      f'Low Stock: {p.product_name if p else inv.product_id}',
            'message':    f'Only {inv.ending_inventory} units remaining at site {inv.site_id}.',
            'product_id': inv.product_id,
        })

    # Delayed shipments (info)
    q_del = (db.session.query(Logistics, Product)
             .join(Product, Logistics.product_id == Product.product_id, isouter=True)
             .filter(Logistics.delivery_status == 'Delayed'))
    if site_id:
        q_del = q_del.filter(Logistics.site_id == site_id)
    for log, p in q_del.limit(20).all():
        alerts.append({
            'level':   'info',
            'title':   f'Delayed Shipment: {p.product_name if p else log.product_id}',
            'message': f'Shipment {log.shipment_id} is delayed.',
            'product_id': log.product_id,
        })

    if level:
        alerts = [a for a in alerts if a['level'] == level]

    return jsonify({'alerts': alerts, 'count': len(alerts)})


# ── Recent sales ──────────────────────────────────────────
@manager_bp.route('/api/recent-sales')
@login_required
@role_required('manager')
@handle_errors
def recent_sales():
    from sqlalchemy import func, extract
    site_id = _manager_site_id()
    mode = request.args.get('mode', 'list')  # 'list' or 'trend'

    if mode == 'trend':
        # Monthly aggregated data for trend chart (last 12 months)
        q = db.session.query(
            func.strftime('%Y-%m', Sale.date).label('month'),
            func.sum(Sale.revenue).label('revenue'),
            func.sum(Sale.units_sold).label('units_sold'),
        )
        if site_id:
            q = q.filter(Sale.site_id == site_id)
        q = q.filter(Sale.date.isnot(None))
        q = q.group_by(func.strftime('%Y-%m', Sale.date))
        q = q.order_by(func.strftime('%Y-%m', Sale.date).desc()).limit(12)
        rows = q.all()
        rows = list(reversed(rows))
        return jsonify({'records': [
            {'date': r.month, 'revenue': float(r.revenue or 0), 'units_sold': int(r.units_sold or 0)}
            for r in rows
        ]})

    # Default: recent 10 individual sales for the list panel
    q = (db.session.query(Sale, Product)
         .join(Product, Sale.product_id == Product.product_id, isouter=True))
    if site_id:
        q = q.filter(Sale.site_id == site_id)
    records = q.order_by(Sale.date.desc()).limit(10).all()
    return jsonify({'records': [{
        'product_name': p.product_name if p else None,
        'units_sold':   s.units_sold,
        'revenue':      float(s.revenue or 0),
        'date':         str(s.date) if s.date else None,
    } for s, p in records]})


# ── Shipments (pending/in-transit/delayed) ────────────────
@manager_bp.route('/shipments')
@login_required
@role_required('manager')
@handle_errors
def shipments_page():
    return render_template('manager/shipments.html')


@manager_bp.route('/api/shipments')
@manager_bp.route('/api/shipments/list')
@login_required
@role_required('manager')
@handle_errors
def shipments():
    from sqlalchemy import func as sqlfunc
    site_id  = _manager_site_id()
    page     = request.args.get('page', 1, type=int)
    per_page = 20
    status   = request.args.get('status', '').strip()
    ttype    = request.args.get('ttype', '').strip()
    q_str    = request.args.get('q', '').strip()
    query = (db.session.query(Logistics, Product, Site)
             .join(Product, Logistics.product_id == Product.product_id, isouter=True)
             .join(Site,    Logistics.site_id    == Site.site_id,       isouter=True))
    if site_id:
        query = query.filter(Logistics.site_id == site_id)
    if status:
        if status == 'Pending':
            query = query.filter(Logistics.delivery_status.in_([
                'Pending', 'Dispatched', 'In Transit', 'Picked Up', 'Out for Delivery'
            ]))
        else:
            query = query.filter(Logistics.delivery_status == status)
    if ttype:
        query = query.filter(Logistics.transportation_type == ttype)
    if q_str:
        query = query.filter(db.or_(
            Product.product_name.ilike(f'%{q_str}%'),
            Logistics.shipment_id.ilike(f'%{q_str}%'),
            Site.site_name.ilike(f'%{q_str}%'),
        ))
    total   = query.with_entities(sqlfunc.count(Logistics.id)).scalar()
    records = query.order_by(Logistics.shipment_date.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({'records': [{
        'shipment_id':         l.shipment_id,
        'product_name':        p.product_name        if p else None,
        'product_id':          l.product_id,
        'site_name':           s.site_name           if s else None,
        'site_id':             l.site_id,
        'quantity':            l.quantity,
        'carrier':             l.transportation_type,
        'transportation_type': l.transportation_type or 'Truck',
        'shipment_date':       str(l.shipment_date)  if l.shipment_date else None,
        'delivery_date':       getattr(l, 'delivery_date', None) or '',
        'delivery_status':     l.delivery_status,
    } for l, p, s in records], 'total': total, 'page': page, 'per_page': per_page})


@manager_bp.route('/api/shipments/stats')
@login_required
@role_required('manager')
@handle_errors
def shipments_stats():
    from sqlalchemy import func as sqlfunc
    site_id = _manager_site_id()
    q = db.session.query(Logistics.delivery_status, sqlfunc.count(Logistics.id)).group_by(Logistics.delivery_status)
    if site_id:
        q = q.filter(Logistics.site_id == site_id)
    counts = {status: cnt for status, cnt in q.all()}
    total  = sum(counts.values())
    return jsonify({'total': total, 'by_status': counts,
                    'in_transit':       counts.get('In Transit', 0),
                    'delivered':        counts.get('Delivered', 0),
                    'pending':          counts.get('Pending', 0),
                    'delayed':          counts.get('Delayed', 0),
                    'cancelled':        counts.get('Cancelled', 0),
                    'dispatched':       counts.get('Dispatched', 0),
                    'picked_up':        counts.get('Picked Up', 0),
                    'out_for_delivery': counts.get('Out for Delivery', 0)})


@manager_bp.route('/api/shipments/<shipment_id>/update-status', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def update_shipment_status(shipment_id):
    from models.db import db as _db
    data       = request.get_json()
    new_status = (data or {}).get('delivery_status', '').strip()
    if not new_status:
        return jsonify({'status': 'error', 'message': 'delivery_status required'}), 400
    valid_statuses = ['Pending', 'Dispatched', 'Picked Up', 'In Transit', 'Out for Delivery', 'Delivered', 'Cancelled', 'Delayed']
    if new_status not in valid_statuses:
        return jsonify({'status': 'error', 'message': f'Invalid status. Valid: {", ".join(valid_statuses)}'}), 400
    ship = Logistics.query.filter_by(shipment_id=shipment_id).first()
    if not ship:
        return jsonify({'status': 'error', 'message': 'Shipment not found'}), 404
    if ship.delivery_status in ('Delivered', 'Cancelled'):
        return jsonify({'status': 'error', 'message': f'Cannot edit — shipment is {ship.delivery_status}'}), 400
    old_status = ship.delivery_status
    ship.delivery_status = new_status
    # If delivered, set delivery date and update inventory flag
    from datetime import date as _date
    if new_status == 'Delivered':
        ship.delivery_date = str(_date.today())
        inv = Inventory.query.filter_by(product_id=ship.product_id, site_id=ship.site_id).first()
        if inv and (inv.ending_inventory or 0) > 0:
            inv.stockout_flag = 'No'
    elif new_status == 'Cancelled':
        # Restore inventory if cancelled after dispatch
        inv = Inventory.query.filter_by(product_id=ship.product_id, site_id=ship.site_id).first()
        if inv:
            inv.ending_inventory = (inv.ending_inventory or 0) + (ship.quantity or 0)
    _db.session.commit()
    log_action('UPDATE', 'Shipments', f'Shipment {shipment_id}', f'Status: {old_status} → {new_status}')
    return jsonify({'status': 'success', 'message': f'Status updated to {new_status}', 'delivery_status': new_status})


# ── Products list (paginated, filterable) ─────────────────
@manager_bp.route('/api/products')
@login_required
@role_required('manager')
@handle_errors
def api_products():
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', PER_PAGE, type=int)
    q_str    = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    query = Product.query
    if q_str:
        query = query.filter(Product.product_name.ilike(f'%{q_str}%'))
    if category:
        query = query.filter_by(category=category)

    # Only show Active products (safe — falls back if column missing)
    try:
        query = query.filter(db.or_(Product.status == 'Active', Product.status == None))
    except Exception:
        pass

    total = query.count()
    items = query.order_by(Product.product_id).offset((page - 1) * per_page).limit(per_page).all()

    site_id = _manager_site_id()
    inv_map = {}
    if site_id:
        try:
            for inv in Inventory.query.filter_by(site_id=site_id).all():
                inv_map[inv.product_id] = inv.ending_inventory or 0
        except Exception:
            pass

    # Also check stock_levels table for more accurate qty
    sl_map = {}
    if site_id:
        try:
            for sl in StockLevel.query.filter_by(site_id=site_id).all():
                sl_map[sl.product_id] = sl.qty_on_hand or 0
        except Exception:
            pass

    def _safe(p, attr, default=None):
        try:
            return getattr(p, attr, default)
        except Exception:
            return default

    products_out = []
    for p in items:
        pid         = _safe(p, 'product_id', '')
        unit_price  = float(_safe(p, 'unit_price', 0) or 0)
        unit_cost   = float(_safe(p, 'unit_cost',  0) or 0)
        # stock_qty: prefer stock_levels, fall back to inventory
        stock_qty   = sl_map.get(pid, inv_map.get(pid))
        products_out.append({
            'product_id':        pid,
            'product_name':      _safe(p, 'product_name', pid),
            'category':          _safe(p, 'category', ''),
            'subcategory':       _safe(p, 'subcategory', ''),
            'uom':               _safe(p, 'uom', 'Unit') or 'Unit',
            'unit_cost':         round(unit_cost,  2),
            'unit_price':        round(unit_price, 2),
            'supplier':          _safe(p, 'supplier', ''),
            'shelf_life':        _safe(p, 'shelf_life', 0),
            'reorder_point':     _safe(p, 'reorder_point', 0) or 0,
            'status':            _safe(p, 'status', 'Active') or 'Active',
            'stock_qty':         stock_qty,
        })

    return jsonify({
        'products': products_out,
        'total': total,
        'page': page,
        'per_page': per_page,
    })


@manager_bp.route('/api/categories')
@login_required
@role_required('manager')
@handle_errors
def api_categories():
    cats = db.session.query(Product.category).distinct().order_by(Product.category).all()
    return jsonify([c[0] for c in cats if c[0]])


# ── Edit product (manager can edit but not add) ───────────
@manager_bp.route('/products/<product_id>/edit', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def edit_product(product_id):
    p    = Product.query.filter_by(product_id=product_id).first_or_404()
    data = request.get_json()
    p.product_name = data.get('product_name', p.product_name)
    p.category     = data.get('category',     p.category)
    p.subcategory  = data.get('subcategory',  p.subcategory)
    p.unit_cost    = float(data.get('unit_cost')  or p.unit_cost)
    p.unit_price   = float(data.get('unit_price') or p.unit_price)
    p.supplier     = data.get('supplier',     p.supplier)
    p.shelf_life   = int(data.get('shelf_life')   or p.shelf_life)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Product updated'})


# ── Delete product ────────────────────────────────────────
@manager_bp.route('/products/<product_id>/delete', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def delete_product(product_id):
    p = Product.query.filter_by(product_id=product_id).first_or_404()
    db.session.delete(p)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Product deleted'})


# ── Inventory list ────────────────────────────────────────
@manager_bp.route('/api/inventory')
@login_required
@role_required('manager')
@handle_errors
def api_inventory():
    site_id  = _manager_site_id()
    page     = request.args.get('page', 1, type=int)
    stockout = request.args.get('stockout', '').strip()
    search   = request.args.get('q', '').strip()

    q = (db.session.query(Inventory, Product, Site)
         .join(Product, Inventory.product_id == Product.product_id, isouter=True)
         .join(Site,    Inventory.site_id    == Site.site_id,       isouter=True))
    if site_id:
        q = q.filter(Inventory.site_id == site_id)
    if stockout == 'yes':
        q = q.filter(Inventory.stockout_flag == 'Yes')
    if search:
        q = q.filter(Product.product_name.ilike(f'%{search}%'))

    # Calculate stats from all matching records
    all_records = q.all()
    total = len(all_records)
    in_stock_count = sum(1 for inv, p, s in all_records if (inv.stockout_flag or 'No') != 'Yes')
    stockout_count = sum(1 for inv, p, s in all_records if (inv.stockout_flag or 'No') == 'Yes')
    replenished_count = sum(1 for inv, p, s in all_records if (inv.replenishment or 0) > 0)

    # Apply pagination
    records = all_records[(page-1)*PER_PAGE:page*PER_PAGE]

    # ── Batch aggregates — eliminates N+1 (60+ queries → 3) ─────────────
    # SalesOrder uses 'site' string field, not product_id/site_id FKs
    # PurchaseOrder uses 'site' string field, not site_id FK
    # Sale uses 'units_sold' not 'quantity_sold'
    prod_ids = list({inv.product_id for inv, p, s in records})
    po_rows = db.session.query(
        PurchaseOrder.product_id,
        func.count(PurchaseOrder.id).label('cnt'),
        func.coalesce(func.sum(PurchaseOrder.total_cost), 0).label('tot')
    ).filter(PurchaseOrder.product_id.in_(prod_ids)).group_by(
        PurchaseOrder.product_id).all()
    po_map = {r.product_id: r for r in po_rows}
    sale_rows = db.session.query(
        Sale.product_id, Sale.site_id,
        func.coalesce(func.sum(Sale.units_sold), 0).label('qty')
    ).filter(Sale.product_id.in_(prod_ids)).group_by(
        Sale.product_id, Sale.site_id).all()
    sale_map = {(r.product_id, r.site_id): int(r.qty) for r in sale_rows}

    # Batch StockLevel for accurate current qty
    sl_rows = StockLevel.query.filter(StockLevel.product_id.in_(prod_ids)).all()
    sl_map  = {(sl.site_id, sl.product_id): (sl.qty_on_hand or 0) for sl in sl_rows}

    result_list = []
    for inv, p, s in records:
        bi       = inv.beginning_inventory or 0
        ei_db    = inv.ending_inventory    or 0
        rep      = inv.replenishment       or 0
        bi_disp  = (ei_db + rep) if (bi == 0 and rep > 0) else bi
        key      = (inv.product_id, inv.site_id)
        po_r     = po_map.get(inv.product_id)
        so_r     = None
        qty_sold = sale_map.get(key, 0)
        # EI formula: BI + Replenishment - Qty Sold
        ei_calc  = bi_disp + rep - qty_sold
        ei_disp  = ei_db if ei_db > 0 else max(0, ei_calc)
        stock_now= sl_map.get((inv.site_id, inv.product_id), ei_disp)
        unit_price = float(p.unit_price or 0) if p else 0
        unit_cost  = float(p.unit_cost  or 0) if p else 0
        margin     = round((unit_price - unit_cost)/unit_price*100,1) if unit_price>0 else 0
        reorder_pt = int(p.reorder_point or 0) if p else 0
        result_list.append({
            'id':                  inv.id,
            'product_id':          inv.product_id,
            'product_name':        p.product_name  if p else inv.product_id,
            'site_id':             inv.site_id,
            'site_name':           s.site_name     if s else inv.site_id,
            'beginning_inventory': bi_disp,
            'ending_inventory':    ei_disp,
            'replenishment':       rep,
            'qty_sold':            qty_sold,
            'stockout_flag':       'Yes' if stock_now == 0 else ('Yes' if inv.stockout_flag=='Yes' else 'No'),
            'unit_cost':           unit_cost,
            'unit_price':          unit_price,
            'profit_margin':       margin,
            'total_sold':          qty_sold,
            'current_stock':       int(stock_now),
            'reorder_point':       reorder_pt,
            'required_stock':      max(0, reorder_pt - int(stock_now)),
            'category':            p.category    if p and hasattr(p,'category')    else '',
            'subcategory':         p.subcategory if p and hasattr(p,'subcategory') else '',
            'supplier':            p.supplier    if p and hasattr(p,'supplier')    else '',
            'so_count':            int(so_r.cnt) if so_r else 0,
            'so_total':            float(so_r.tot) if so_r else 0.0,
            'po_count':            int(po_r.cnt) if po_r else 0,
            'po_total':            float(po_r.tot) if po_r else 0.0,
        })
    return jsonify({
        'records': result_list,
        'total': total, 'page': page, 'per_page': PER_PAGE,
        'stats': {
            'total_records': total,
            'in_stock': in_stock_count,
            'stockouts': stockout_count,
            'replenished': replenished_count
        }
    })


# ── Stock adjustment ──────────────────────────────────────
@manager_bp.route('/api/adjust-stock', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def adjust_stock():
    data    = request.get_json()
    pid     = (data.get('product_id') or '').strip()
    adj_type= data.get('adjustment_type', 'add')
    qty     = int(data.get('quantity') or 0)
    site_id = _manager_site_id()

    if not pid or not qty:
        return jsonify({'status': 'error', 'message': 'Product ID and quantity required'}), 400

    inv = Inventory.query.filter_by(product_id=pid, site_id=site_id).first() if site_id else \
          Inventory.query.filter_by(product_id=pid).first()
    if not inv:
        return jsonify({'status': 'error', 'message': f'No inventory record found for product {pid}'}), 404

    if adj_type == 'add':
        inv.ending_inventory = (inv.ending_inventory or 0) + qty
    elif adj_type == 'remove':
        inv.ending_inventory = max(0, (inv.ending_inventory or 0) - qty)
    elif adj_type == 'set':
        inv.ending_inventory = qty

    inv.stockout_flag = 'Yes' if (inv.ending_inventory or 0) == 0 else 'No'
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Stock adjusted. New level: {inv.ending_inventory}'})


# ── Sales list ────────────────────────────────────────────
@manager_bp.route('/api/sales')
@login_required
@role_required('manager')
@handle_errors
def api_sales():
    site_id = _manager_site_id()
    page    = request.args.get('page', 1, type=int)
    q_str   = request.args.get('q', '').strip()

    q = (db.session.query(Sale, Product)
         .join(Product, Sale.product_id == Product.product_id, isouter=True))
    if site_id:
        q = q.filter(Sale.site_id == site_id)
    if q_str:
        q = q.filter(Product.product_name.ilike(f'%{q_str}%'))

    summary_q = db.session.query(
        func.sum(Sale.revenue).label('total_revenue'),
        func.sum(Sale.units_sold).label('total_units'),
        func.sum(Sale.discounts).label('total_discounts'),
        func.sum(Sale.returns).label('total_returns'),
    )
    if site_id:
        summary_q = summary_q.filter(Sale.site_id == site_id)
    summary = summary_q.first()

    total   = q.count()
    records = q.order_by(Sale.date.desc()).offset((page-1)*PER_PAGE).limit(PER_PAGE).all()
    return jsonify({
        'records': [{
            'product_name': p.product_name if p else None,
            'units_sold':   s.units_sold,
            'revenue':      float(s.revenue   or 0),
            'discounts':    float(s.discounts  or 0),
            'returns':      s.returns,
            'date':         str(s.date) if s.date else None,
        } for s, p in records],
        'summary': {
            'total_revenue':   float(summary.total_revenue   or 0),
            'total_units':     int(summary.total_units        or 0),
            'total_discounts': float(summary.total_discounts  or 0),
            'total_returns':   int(summary.total_returns       or 0),
        },
        'total': total, 'page': page, 'per_page': PER_PAGE,
    })


# ── Site info ─────────────────────────────────────────────
@manager_bp.route('/api/site')
@login_required
@role_required('manager')
@handle_errors
def api_site():
    site_id = _manager_site_id()
    if not site_id:
        return jsonify({'site': None})
    s = Site.query.filter_by(site_id=site_id).first()
    if not s:
        return jsonify({'site': None})
    return jsonify({'site': {
        'site_id':    s.site_id,
        'site_name':  s.site_name,
        'site_format':s.site_format,
        'region':     s.region,
        'city':       s.city,
        'store_size': s.store_size,
        'open_date':  str(s.open_date) if s.open_date else None,
        'status':     s.status,
    }})


# ── Purchase Orders (DB-backed) ───────────────────────────
@manager_bp.route('/api/purchase-orders', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def get_purchase_orders():
    page     = request.args.get('page', 1, type=int)
    status_f = request.args.get('status', '').strip()
    uid      = session['user_id']
    query    = PurchaseOrder.query.filter_by(role='manager', manager_user_id=uid)
    if status_f:
        query = query.filter_by(status=status_f)
    total  = query.count()
    orders = query.order_by(PurchaseOrder.id.desc()).offset((page-1)*PER_PAGE).limit(PER_PAGE).all()
    records = []
    for o in orders:
        od = o.to_dict()
        p = Product.query.filter_by(product_id=o.product_id).first()
        od['product_name'] = p.product_name if p else o.product_id
        records.append(od)
    return jsonify({'orders': records, 'total': total, 'page': page, 'per_page': PER_PAGE})


@manager_bp.route('/api/purchase-orders', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def create_purchase_order():
    data = request.get_json()
    pid  = (data.get('product_id') or '').strip()
    qty  = int(data.get('quantity') or 0)
    if not pid or not qty:
        return jsonify({'status': 'error', 'message': 'Product ID and quantity required'}), 400
    # Fetch unit_cost from product catalogue
    prod = Product.query.filter_by(product_id=pid).first()
    unit_cost  = float(prod.unit_cost  or 0) if prod else float(data.get('unit_cost') or 0)
    product_name = prod.product_name if prod else pid
    supplier_name = prod.supplier if prod else (data.get('supplier') or '')
    total_cost = round(unit_cost * qty, 2)
    po_num = _random_id('PO-')
    po = PurchaseOrder(
        po_number        = po_num,
        product_id       = pid,
        product_name     = product_name,
        supplier         = supplier_name,
        quantity         = qty,
        unit_cost        = unit_cost,
        total_cost       = total_cost,
        expected_delivery= data.get('delivery_date', ''),
        status           = 'Pending',
        created_by       = session.get('username', str(session['user_id'])),
        created_at       = str(date.today()),
        role             = 'manager',
        manager_user_id  = session['user_id'],
        site             = _manager_site_id() or '',
    )
    db.session.add(po)
    db.session.commit()
    log_action('CREATE', 'Purchase Orders', f'PO {po_num}', f'Product: {pid}, Qty: {qty}, Cost: {unit_cost}')
    return jsonify({'status': 'success', 'message': f'Purchase order {po_num} created'})


@manager_bp.route('/api/purchase-orders/<po_number>/approve', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def approve_purchase_order(po_number):
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'PO not found'}), 404
    po.status      = 'Approved'
    po.approved_at = str(date.today())
    # Auto-update inventory when PO is approved
    inv_updated = False
    try:
        site_id = (po.site or '').split(' - ')[0].strip() if ' - ' in (po.site or '') else (po.site or '').strip()
        qty = po.quantity or 0
        if po.product_id and site_id and qty > 0:
            inv = Inventory.query.filter_by(product_id=po.product_id, site_id=site_id).first()
            if inv:
                inv.ending_inventory    = (inv.ending_inventory    or 0) + qty
                inv.beginning_inventory = (inv.beginning_inventory or 0) + qty
                inv.replenishment       = (inv.replenishment       or 0) + qty
                if inv.ending_inventory > 0:
                    inv.stockout_flag = 'No'
            else:
                db.session.add(Inventory(site_id=site_id, product_id=po.product_id,
                    beginning_inventory=qty, ending_inventory=qty,
                    replenishment=qty, stockout_flag='No'))
            inv_updated = True
    except Exception as ex:
        print(f'PO approve inventory error: {ex}')
    db.session.commit()
    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}', f'Approved, inventory +{po.quantity}')
    return jsonify({'status': 'success', 'message': f'{po_number} approved', 'inventory_updated': inv_updated, 'qty_added': po.quantity})


@manager_bp.route('/api/purchase-orders/<po_number>/cancel', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def cancel_purchase_order(po_number):
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'PO not found'}), 404
    po.status = 'Cancelled'
    db.session.commit()
    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}', 'Status → Cancelled')
    return jsonify({'status': 'success', 'message': f'{po_number} cancelled'})


# ── Sales Orders (DB-backed) ──────────────────────────────
@manager_bp.route('/api/sales-orders', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def get_sales_orders():
    page     = request.args.get('page', 1, type=int)
    status_f = request.args.get('status', '').strip()
    uid      = session['user_id']
    query    = SalesOrder.query.filter_by(role='manager', manager_user_id=uid)
    if status_f:
        query = query.filter_by(status=status_f)
    total  = query.count()
    orders = query.order_by(SalesOrder.id.desc()).offset((page - 1) * PER_PAGE).limit(PER_PAGE).all()
    records = []
    for o in orders:
        od = o.to_dict()
        try:
            items = json.loads(o.items_json or '[]')
        except Exception:
            items = []

        # Total quantity across all items
        total_qty  = sum(int(it.get('quantity', 0)) for it in items)

        # Primary product display name
        first_pid  = items[0].get('product_id', '') if items else ''
        first_name = items[0].get('product_name', '') if items else ''
        if not first_name and first_pid:
            p = Product.query.filter_by(product_id=first_pid).first()
            first_name = p.product_name if p else first_pid
        if len(items) > 1:
            first_name = f'{first_name} (+{len(items) - 1} more)'

        od['product_name'] = first_name or first_pid or '--'
        od['product_id']   = first_pid
        od['quantity']     = total_qty
        od['item_count']   = len(items)
        od['items']        = items
        od['customer_id']  = o.customer_id or o.customer or '--'
        od['discount']     = items[0].get('discount', 0) if items else 0
        records.append(od)
    return jsonify({'orders': records, 'total': total, 'page': page, 'per_page': PER_PAGE})


@manager_bp.route('/api/sales-orders', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def create_sales_order():
    data        = request.get_json()
    customer_id = (data.get('customer_id') or '').strip()
    site_val    = (data.get('site') or '').strip()
    notes       = data.get('notes', '')

    # Support both legacy single-product payload and new multi-item array
    items_raw = data.get('items', [])
    if not items_raw:
        # Legacy: single product_id / quantity fields
        pid = (data.get('product_id') or '').strip()
        qty = int(data.get('quantity') or 0)
        if not pid or not qty:
            return jsonify({'status': 'error', 'message': 'Product ID and quantity required'}), 400
        items_raw = [{'product_id': pid, 'quantity': qty}]

    # Resolve site_id for stock checks
    site_id = _manager_site_id() or site_val.split(' - ')[0].strip()

    # Validate stock for each item and build items list with amounts
    total_amount = 0.0
    items_out    = []
    for it in items_raw:
        pid = (it.get('product_id') or '').strip()
        qty = int(it.get('quantity') or 0)
        if not pid or qty <= 0:
            continue
        p = Product.query.filter_by(product_id=pid).first()
        unit_price = float(getattr(p, 'unit_price', 0) or 0) if p else 0.0
        discount   = float(it.get('discount', 0) or 0)
        line_total = round(unit_price * qty * (1 - discount / 100), 2)
        total_amount += line_total

        # Stock check (non-blocking — warn but allow if no inventory record)
        inv = Inventory.query.filter_by(product_id=pid, site_id=site_id).first()
        avail = inv.ending_inventory or 0 if inv else None
        if avail is not None and avail < qty:
            return jsonify({
                'status': 'error',
                'message': f'Insufficient stock for {p.product_name if p else pid}. Available: {avail}, Requested: {qty}'
            }), 400

        items_out.append({
            'product_id':   pid,
            'product_name': p.product_name if p else pid,
            'quantity':     qty,
            'unit_price':   unit_price,
            'discount':     discount,
            'line_total':   line_total,
        })

    if not items_out:
        return jsonify({'status': 'error', 'message': 'No valid items in order'}), 400

    so_num = _random_id('SO-')
    # Resolve customer name from customer_id
    customer_name = customer_id
    try:
        cust = Customer.query.filter_by(customer_id=customer_id).first()
        if cust:
            customer_name = getattr(cust, 'customer_id', customer_id)
    except Exception:
        pass

    so = SalesOrder(
        so_number       = so_num,
        customer_id     = customer_id,
        customer        = customer_name,
        site            = site_val or site_id,
        items_json      = json.dumps(items_out),
        total_amount    = round(total_amount, 2),
        notes           = notes,
        status          = 'Pending',
        created_by      = session.get('username', str(session['user_id'])),
        created_at      = str(date.today()),
        role            = 'manager',
        manager_user_id = session['user_id'],
    )
    db.session.add(so)
    db.session.commit()
    log_action('CREATE_SALES_ORDER', 'Sales Orders', f'SO {so_num}',
               f'Items: {len(items_out)}, Total: {total_amount}, Site: {site_id}')
    return jsonify({'status': 'success', 'message': f'Sales order {so_num} created', 'so_number': so_num})


@manager_bp.route('/api/sales-orders/<so_number>/cancel', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def cancel_sales_order(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'SO not found'}), 404
    so.status = 'Cancelled'
    db.session.commit()
    log_action('UPDATE', 'Sales Orders', f'SO {so_number}', 'Status → Cancelled')
    return jsonify({'status': 'success', 'message': f'{so_number} cancelled'})


# ── Promotions (view only) ────────────────────────────────
@manager_bp.route('/api/promotions')
@login_required
@role_required('manager')
@handle_errors
def api_promotions():
    site_id = _manager_site_id()
    page    = request.args.get('page', 1, type=int)
    q = (db.session.query(Promotion, Product)
         .join(Product, Promotion.product_id == Product.product_id, isouter=True))
    if site_id:
        q = q.filter(Promotion.site_id == site_id)
    total   = q.count()
    records = q.order_by(Promotion.start_date.desc()).offset((page-1)*PER_PAGE).limit(PER_PAGE).all()
    # Also join Site for site_name
    return jsonify({
        'records': [{
            'id':                  promo.id,
            'product_id':          promo.product_id,
            'site_id':             promo.site_id,
            'product_name':        p.product_name if p else promo.product_id,
            'site_name':           Site.query.filter_by(site_id=promo.site_id).first().site_name if promo.site_id else 'All Sites',
            'promotion_type':      promo.discount_type,
            'discount_percentage': float(promo.discount_amount or 0),
            'start_date':          str(promo.start_date) if promo.start_date else None,
            'end_date':            str(promo.end_date)   if promo.end_date   else None,
        } for promo, p in records],
        'total': total, 'page': page, 'per_page': PER_PAGE,
    })



# ── Suppliers (view + add for manager) ───────────────────
@manager_bp.route('/suppliers')
@login_required
@role_required('manager')
@handle_errors
def suppliers():
    return render_template('manager/suppliers.html')


@manager_bp.route('/api/suppliers')
@login_required
@role_required('manager')
@handle_errors
def api_suppliers():
    sups = Supplier.query.order_by(Supplier.supplier_name).all()
    return jsonify({'suppliers': [s.to_dict() for s in sups]})


@manager_bp.route('/api/suppliers/add', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def add_supplier_manager():
    from models.db import db
    from sqlalchemy import func
    data  = request.get_json()
    name  = (data.get('supplier_name') or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    if not name:
        return jsonify({'status': 'error', 'message': 'Supplier name is required'}), 400
    if Supplier.query.filter_by(supplier_name=name).first():
        return jsonify({'status': 'error', 'message': 'Supplier with this name already exists'}), 400
    last = db.session.query(func.count(Supplier.id)).scalar() or 0
    sup_id = f'supplier{last + 1}'
    s = Supplier(supplier_id=sup_id, supplier_name=name, email=email or None, phone=phone or None)
    db.session.add(s)
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Supplier "{name}" added', 'supplier': s.to_dict()})


# ── Customers ─────────────────────────────────────────────
@manager_bp.route('/customers')
@login_required
@role_required('manager')
@handle_errors
def customers():
    return render_template('manager/customers.html')


@manager_bp.route('/customers/stats')
@login_required
@role_required('manager')
@handle_errors
def customer_stats():
    from sqlalchemy import func
    total     = Customer.query.count()
    avg_spend = float(db.session.query(func.avg(Customer.average_spend)).scalar() or 0)
    avg_clv   = float(db.session.query(func.avg(Customer.clv)).scalar() or 0)
    avg_csat  = float(db.session.query(func.avg(Customer.csat)).scalar() or 0)
    avg_nps   = float(db.session.query(func.avg(Customer.nps)).scalar() or 0)
    by_gender = db.session.query(Customer.gender, func.count(Customer.id)).group_by(Customer.gender).all()
    by_income = db.session.query(Customer.income_bracket, func.count(Customer.id)).group_by(Customer.income_bracket).all()
    return jsonify({
        'total': total, 'avg_spend': avg_spend, 'avg_clv': avg_clv,
        'avg_csat': avg_csat, 'avg_nps': avg_nps,
        'by_gender': [{'label': r[0] or 'Unknown', 'count': r[1]} for r in by_gender],
        'by_income': [{'label': r[0] or 'Unknown', 'count': r[1]} for r in by_income],
    })


@manager_bp.route('/customers/list')
@login_required
@role_required('manager')
@handle_errors
def customer_list():
    page     = request.args.get('page', 1, type=int)
    q        = request.args.get('q', '').strip()
    gender_f = request.args.get('gender', '').strip()
    income_f = request.args.get('income', '').strip()
    per_page = 20
    query = Customer.query
    if q:        query = query.filter(Customer.customer_id.ilike(f'%{q}%'))
    if gender_f: query = query.filter_by(gender=gender_f)
    if income_f: query = query.filter_by(income_bracket=income_f)
    total = query.count()
    items = query.order_by(Customer.id).offset((page - 1) * per_page).limit(per_page).all()
    return jsonify({'customers': [c.to_dict() for c in items], 'total': total, 'page': page, 'per_page': per_page})


# ── Audit Log ─────────────────────────────────────────────
@manager_bp.route('/audit-log')
@login_required
@role_required('manager')
def audit_log():
    return render_template('manager/audit_log.html')


@manager_bp.route('/api/audit-log')
@login_required
@role_required('manager')
@handle_errors
def get_audit_log():
    """
    Returns paginated audit-log entries.
    Falls back to an in-memory demo dataset when no AuditLog model is present.
    """
    page      = request.args.get('page', 1, type=int)
    per_page  = request.args.get('per_page', 20, type=int)
    action_f  = request.args.get('action', '').strip().upper()
    module_f  = request.args.get('module', '').strip()
    q         = request.args.get('q', '').strip().lower()
    date_from = request.args.get('date_from', '').strip()
    date_to   = request.args.get('date_to', '').strip()

    # Try real AuditLog model first
    try:
        from models.records import AuditLog
        query = db.session.query(AuditLog)
        if action_f: query = query.filter(AuditLog.action == action_f)
        if module_f: query = query.filter(AuditLog.module == module_f)
        if q:
            query = query.filter(
                db.or_(
                    AuditLog.user.ilike(f'%{q}%'),
                    AuditLog.detail.ilike(f'%{q}%'),
                    AuditLog.resource.ilike(f'%{q}%'),
                )
            )
        if date_from: query = query.filter(db.func.date(AuditLog.timestamp) >= date_from)
        if date_to:   query = query.filter(db.func.date(AuditLog.timestamp) <= date_to)
        total = query.count()
        records = query.order_by(AuditLog.timestamp.desc()).offset((page-1)*per_page).limit(per_page).all()
        logs = [{
            'id':        r.id,
            'timestamp': r.to_dict()['timestamp'],
            'user':      r.user,
            'action':    r.action,
            'module':    r.module,
            'resource':  r.resource,
            'detail':    r.detail,
            'ip':        r.ip_address,
        } for r in records]
        return jsonify({'logs': logs, 'total': total, 'page': page, 'per_page': per_page})
    except Exception:
        pass

    # Fallback: empty dataset (client side generates demo)
    return jsonify({'logs': [], 'total': 0, 'page': page, 'per_page': per_page, 'demo': True})


# ═══════════════════════════════════════════════════════════
#  MISSING FEATURES — ADDED BY FIX PASS
# ═══════════════════════════════════════════════════════════

# ── SO Confirm ────────────────────────────────────────────
import _string as _string_mod
import string as _str_mod

@manager_bp.route('/api/sales-orders/<so_number>/confirm', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def confirm_sales_order_manager(so_number):
    """
    Confirm a Pending SO.
    - Deducts stock from inventory.ending_inventory
    - Creates Logistics shipment record(s)
    - Sets status = Confirmed + confirmed_at timestamp
    """
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'SO not found'}), 404
    if so.status != 'Pending':
        return jsonify({'status': 'error', 'message': 'Only Pending orders can be confirmed'}), 400

    site_raw = so.site or ''
    site_id  = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()
    items    = json.loads(so.items_json or '[]')
    shipments_created = []

    try:
        for item in items:
            product_id = item.get('product_id', '')
            qty        = int(item.get('quantity', 0))
            if not product_id or qty <= 0:
                continue

            # Deduct from inventory
            inv = Inventory.query.filter_by(product_id=product_id, site_id=site_id).first()
            if inv:
                inv.ending_inventory = max(0, (inv.ending_inventory or 0) - qty)
                if inv.ending_inventory == 0:
                    inv.stockout_flag = 'Yes'

            # Also deduct from stock_levels if present
            sl = StockLevel.query.filter_by(site_id=site_id, product_id=product_id).first()
            if sl:
                sl.qty_on_hand = max(0, sl.qty_on_hand - qty)

            # Create StockMovement
            db.session.add(StockMovement(
                site_id       = site_id,
                product_id    = product_id,
                movement_type = 'SaleOut',
                qty_change    = -qty,
                reference_id  = so_number,
                created_by    = session.get('user_id'),
            ))

            # Create Logistics record
            shipment_id = 'SHP-' + ''.join(__import__('random').choices(
                __import__('string').ascii_uppercase + __import__('string').digits, k=8))
            db.session.add(Logistics(
                shipment_id         = shipment_id,
                site_id             = site_id,
                product_id          = product_id,
                shipment_date       = date.today(),
                quantity            = qty,
                delivery_status     = 'Pending',
                transportation_type = so.dispatch_type or 'Truck',
                so_id               = so.id,
                so_number           = so_number,
            ))
            item['shipment_id'] = shipment_id
            shipments_created.append({'shipment_id': shipment_id, 'product_id': product_id})

        so.items_json   = json.dumps(items)
        so.status       = 'Processing'
        so.confirmed_at = str(date.today())
        db.session.commit()
        log_action('UPDATE', 'Sales Orders', f'SO {so_number}',
                   f'Order moved to Processing by {session.get("username")}. Shipments: {len(shipments_created)}')
    except Exception as ex:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(ex)}), 500

    return jsonify({'status': 'success', 'confirmed_at': so.confirmed_at,
                    'shipments': shipments_created})


# ── SO Dispatch (update dispatch type + set Dispatched) ───
@manager_bp.route('/api/sales-orders/<so_number>/dispatch', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def dispatch_sales_order_manager(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'SO not found'}), 404
    d             = request.get_json() or {}
    dispatch_type = d.get('dispatch_type', 'Truck')
    so.status        = 'Dispatched'
    so.dispatch_type = dispatch_type
    so.dispatched_at = str(date.today())
    try:
        items = json.loads(so.items_json or '[]')
        for item in items:
            sid = item.get('shipment_id')
            if sid:
                rec = Logistics.query.filter_by(shipment_id=sid).first()
                if rec:
                    rec.transportation_type = dispatch_type
                    rec.delivery_status = 'In Transit'
        db.session.commit()
        log_action('UPDATE', 'Sales Orders', f'SO {so_number}', f'Dispatched via {dispatch_type}')
    except Exception:
        db.session.rollback()
    return jsonify({'status': 'success', 'dispatch_type': dispatch_type})


# ── SO Cancel with reason ─────────────────────────────────
@manager_bp.route('/api/sales-orders/<so_number>/cancel', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def cancel_sales_order_manager(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'SO not found'}), 404
    d = request.get_json() or {}
    so.status        = 'Cancelled'
    so.cancelled_at  = str(date.today())
    so.cancel_reason = d.get('cancel_reason', '')
    db.session.commit()
    log_action('UPDATE', 'Sales Orders', f'SO {so_number}',
               f'Cancelled by manager. Reason: {so.cancel_reason}')
    return jsonify({'status': 'success', 'message': f'{so_number} cancelled'})


# ── SO Tracking ───────────────────────────────────────────
@manager_bp.route('/api/sales-orders/<so_number>/tracking', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def get_so_tracking_manager(so_number):
    """Full tracking timeline for a Sales Order."""
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'SO not found'}), 404
    shipments = []
    items = json.loads(so.items_json or '[]')
    for item in items:
        sid = item.get('shipment_id')
        if not sid:
            continue
        rec = Logistics.query.filter_by(shipment_id=sid).first()
        if rec:
            prod = Product.query.filter_by(product_id=rec.product_id).first()
            shipments.append({
                'shipment_id':            rec.shipment_id,
                'product_id':             rec.product_id,
                'product_name':           prod.product_name if prod else rec.product_id,
                'quantity':               rec.quantity,
                'shipment_date':          str(rec.shipment_date) if rec.shipment_date else None,
                'delivery_status':        rec.delivery_status,
                'transportation_type':    rec.transportation_type,
                'estimated_delivery':     str(rec.estimated_delivery) if rec.estimated_delivery else None,
                'tracking_notes':         rec.tracking_notes or '',
                'tracking_status_updated': rec.tracking_status_updated.isoformat() if rec.tracking_status_updated else None,
                'site_id':                rec.site_id,
            })
    in_transit = any(s.get('delivery_status') == 'In Transit' for s in shipments)
    timeline = [
        {'stage': 'Order Placed', 'done': True,                        'date': so.created_at   or ''},
        {'stage': 'Processing',   'done': bool(so.confirmed_at),        'date': so.confirmed_at or ''},
        {'stage': 'Shipped',      'done': bool(so.dispatched_at),       'date': so.dispatched_at or ''},
        {'stage': 'In Transit',   'done': in_transit,                   'date': in_transit and (so.dispatched_at or '') or ''},
        {'stage': 'Delivered',    'done': so.status == 'Delivered',     'date': ''},
    ]
    return jsonify({'status': 'success', 'so_status': so.status,
                    'shipments': shipments, 'timeline': timeline})


@manager_bp.route('/api/logistics/<int:log_id>/tracking', methods=['PUT'])
@login_required
@role_required('manager')
@handle_errors
def update_logistics_tracking(log_id):
    """Update delivery status, notes, and estimated delivery for a shipment."""
    from datetime import datetime as _dt, date as _d
    rec = db.session.get(Logistics, log_id)
    if not rec:
        return jsonify({'status': 'error', 'message': 'Shipment not found'}), 404
    d = request.get_json() or {}
    if 'delivery_status'    in d: rec.delivery_status    = d['delivery_status']
    if 'tracking_notes'     in d: rec.tracking_notes     = d['tracking_notes']
    if 'estimated_delivery' in d:
        try:    rec.estimated_delivery = _d.fromisoformat(d['estimated_delivery'])
        except: pass
    rec.tracking_status_updated = _dt.utcnow()
    db.session.commit()
    log_action('UPDATE', 'Shipments', f'Shipment {rec.shipment_id}',
               f'Tracking: {rec.delivery_status}')
    return jsonify({'status': 'success', 'shipment': rec.to_dict()})


# ── PO Reject ─────────────────────────────────────────────
@manager_bp.route('/api/purchase-orders/<po_number>/reject', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def reject_purchase_order_manager(po_number):
    """Reject a PO — sends it back to Draft with a rejection reason."""
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'PO not found'}), 404
    if po.status not in ('Pending', 'Draft'):
        return jsonify({'status': 'error', 'message': 'Only Pending/Draft POs can be rejected'}), 400
    d = request.get_json() or {}
    po.status           = 'Draft'
    po.rejection_reason = d.get('rejection_reason', '')
    db.session.commit()
    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}',
               f'Rejected: {po.rejection_reason}')
    return jsonify({'status': 'success', 'message': f'{po_number} rejected'})


# ── PO Receive Goods (with StockMovement) ─────────────────
@manager_bp.route('/api/purchase-orders/<po_number>/receive', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def receive_purchase_order_manager(po_number):
    """
    Receive goods for an Approved PO.
    Updates inventory, creates StockLevel row, and records a StockMovement (PurchaseIn).
    """
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'PO not found'}), 404
    if po.status != 'Approved':
        return jsonify({'status': 'error', 'message': 'Only Approved POs can be received'}), 400

    d       = request.get_json() or {}
    qty     = int(d.get('qty_received', po.quantity) or po.quantity)
    remarks = d.get('remarks', '')

    site_raw = po.site or ''
    site_id  = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()

    if po.product_id and site_id and qty > 0:
        inv = Inventory.query.filter_by(product_id=po.product_id, site_id=site_id).first()
        if inv:
            inv.ending_inventory    = (inv.ending_inventory    or 0) + qty
            inv.beginning_inventory = (inv.beginning_inventory or 0) + qty
            inv.replenishment       = (inv.replenishment       or 0) + qty
            if inv.ending_inventory > 0:
                inv.stockout_flag = 'No'
        else:
            db.session.add(Inventory(site_id=site_id, product_id=po.product_id,
                beginning_inventory=qty, ending_inventory=qty,
                replenishment=qty, stockout_flag='No'))

        # Update StockLevel
        sl = StockLevel.query.filter_by(site_id=site_id, product_id=po.product_id).first()
        if sl:
            sl.qty_on_hand += qty
        else:
            db.session.add(StockLevel(site_id=site_id, product_id=po.product_id, qty_on_hand=qty))

        # Record StockMovement
        db.session.add(StockMovement(
            site_id       = site_id,
            product_id    = po.product_id,
            movement_type = 'PurchaseIn',
            qty_change    = qty,
            reference_id  = po_number,
            remarks       = remarks,
            created_by    = session.get('user_id'),
        ))

    po.status      = 'Received'
    po.received_at = str(date.today())
    db.session.commit()
    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}',
               f'Goods received qty={qty}, site={site_id}')
    return jsonify({'status': 'success', 'message': f'Goods received for {po_number}',
                    'qty_received': qty})


# ── Inventory CREATE ──────────────────────────────────────
@manager_bp.route('/api/inventory', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def create_inventory():
    """Create a new inventory record for a product at a site."""
    d = request.get_json()
    site_id    = (d.get('site_id') or '').strip()
    product_id = (d.get('product_id') or '').strip()
    if not site_id or not product_id:
        return jsonify({'status': 'error', 'message': 'site_id and product_id are required'}), 400
    if Inventory.query.filter_by(site_id=site_id, product_id=product_id).first():
        return jsonify({'status': 'error', 'message': 'Inventory record already exists for this site/product'}), 400
    inv = Inventory(
        site_id             = site_id,
        product_id          = product_id,
        beginning_inventory = int(d.get('beginning_inventory', 0) or 0),
        ending_inventory    = int(d.get('ending_inventory',    0) or 0),
        replenishment       = int(d.get('replenishment',       0) or 0),
        stockout_flag       = d.get('stockout_flag', 'No'),
    )
    db.session.add(inv)
    db.session.commit()
    log_action('CREATE', 'Inventory', f'{site_id}/{product_id}',
               f'beginning={inv.beginning_inventory}, ending={inv.ending_inventory}')
    return jsonify({'status': 'success', 'id': inv.id})


# ── Inventory UPDATE ──────────────────────────────────────
@manager_bp.route('/api/inventory/<int:inv_id>', methods=['PUT'])
@login_required
@role_required('manager')
@handle_errors
def update_inventory(inv_id):
    inv = db.session.get(Inventory, inv_id)
    if not inv:
        return jsonify({'status': 'error', 'message': 'Inventory record not found'}), 404
    d = request.get_json()
    if 'beginning_inventory' in d: inv.beginning_inventory = int(d['beginning_inventory'] or 0)
    if 'ending_inventory'    in d: inv.ending_inventory    = int(d['ending_inventory']    or 0)
    if 'replenishment'       in d: inv.replenishment       = int(d['replenishment']       or 0)
    if 'stockout_flag'       in d: inv.stockout_flag       = d['stockout_flag']
    db.session.commit()
    log_action('UPDATE', 'Inventory', f'{inv.site_id}/{inv.product_id}',
               f'ending={inv.ending_inventory}, stockout={inv.stockout_flag}')
    return jsonify({'status': 'success'})


# ── Stock Level Query ─────────────────────────────────────
@manager_bp.route('/api/stock-levels', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def get_stock_levels():
    """Query current stock levels, optionally filtered by site_id or product_id."""
    site_id    = request.args.get('site_id', '').strip()
    product_id = request.args.get('product_id', '').strip()
    q = StockLevel.query
    if site_id:    q = q.filter_by(site_id=site_id)
    if product_id: q = q.filter_by(product_id=product_id)
    rows = q.all()
    return jsonify({'stock_levels': [r.to_dict() for r in rows], 'total': len(rows)})


@manager_bp.route('/api/stock-movements', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def get_stock_movements():
    """Query stock movement history filtered by product_id or site_id."""
    site_id    = request.args.get('site_id', '').strip()
    product_id = request.args.get('product_id', '').strip()
    ref        = request.args.get('reference_id', '').strip()
    q = StockMovement.query
    if site_id:    q = q.filter_by(site_id=site_id)
    if product_id: q = q.filter_by(product_id=product_id)
    if ref:        q = q.filter_by(reference_id=ref)
    rows = q.order_by(StockMovement.created_at.desc()).limit(200).all()
    return jsonify({'movements': [r.to_dict() for r in rows], 'total': len(rows)})


# ── Promotion CRUD ────────────────────────────────────────
@manager_bp.route('/api/promotions', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def create_promotion():
    d = request.get_json()
    promo_id = (d.get('promotion_id') or '').strip()
    if not promo_id:
        import random, string
        promo_id = 'PROMO-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    if Promotion.query.filter_by(promotion_id=promo_id).first():
        return jsonify({'status': 'error', 'message': 'Promotion ID already exists'}), 400
    from datetime import date as _d
    p = Promotion(
        promotion_id    = promo_id,
        product_id      = d.get('product_id', ''),
        site_id         = d.get('site_id', ''),
        start_date      = _d.fromisoformat(d['start_date']) if d.get('start_date') else None,
        end_date        = _d.fromisoformat(d['end_date'])   if d.get('end_date')   else None,
        discount_type   = d.get('discount_type', 'Percentage'),
        discount_amount = float(d.get('discount_amount', 0) or 0),
    )
    db.session.add(p)
    db.session.commit()
    log_action('CREATE', 'Promotions', f'Promo {promo_id}',
               f'Product: {p.product_id}, Discount: {p.discount_amount}')
    return jsonify({'status': 'success', 'promotion_id': promo_id})


@manager_bp.route('/api/promotions/<int:promo_id>', methods=['PUT'])
@login_required
@role_required('manager')
@handle_errors
def update_promotion(promo_id):
    p = db.session.get(Promotion, promo_id)
    if not p:
        return jsonify({'status': 'error', 'message': 'Promotion not found'}), 404
    d = request.get_json()
    from datetime import date as _d
    if 'product_id'      in d: p.product_id      = d['product_id']
    if 'site_id'         in d: p.site_id         = d['site_id']
    if 'discount_type'   in d: p.discount_type   = d['discount_type']
    if 'discount_amount' in d: p.discount_amount = float(d['discount_amount'] or 0)
    if 'start_date'      in d:
        try:    p.start_date = _d.fromisoformat(d['start_date'])
        except: pass
    if 'end_date'        in d:
        try:    p.end_date   = _d.fromisoformat(d['end_date'])
        except: pass
    db.session.commit()
    return jsonify({'status': 'success'})


@manager_bp.route('/api/promotions/<int:promo_id>', methods=['DELETE'])
@login_required
@role_required('manager')
@handle_errors
def delete_promotion(promo_id):
    p = db.session.get(Promotion, promo_id)
    if not p:
        return jsonify({'status': 'error', 'message': 'Promotion not found'}), 404
    pid = p.promotion_id
    db.session.delete(p)
    db.session.commit()
    log_action('DELETE', 'Promotions', f'Promo {pid}', '')
    return jsonify({'status': 'success'})


@manager_bp.route('/api/promotions/lookup', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def promotion_lookup():
    """
    Find the best active promotion for a product+site combination.
    Query params: product_id, site_id, promo_code (optional)
    Returns the promotion with the highest discount_amount.
    """
    from datetime import date as _d
    product_id = request.args.get('product_id', '').strip()
    site_id    = request.args.get('site_id', '').strip()
    promo_code = request.args.get('promo_code', '').strip()
    today = _d.today()
    q = Promotion.query.filter(
        Promotion.start_date <= today,
        Promotion.end_date   >= today,
    )
    if product_id: q = q.filter_by(product_id=product_id)
    if site_id:    q = q.filter_by(site_id=site_id)
    if promo_code: q = q.filter_by(promotion_id=promo_code)
    best = q.order_by(Promotion.discount_amount.desc()).first()
    if not best:
        return jsonify({'status': 'ok', 'promotion': None, 'message': 'No active promotion found'})
    return jsonify({'status': 'ok', 'promotion': {
        'promotion_id':    best.promotion_id,
        'discount_type':   best.discount_type,
        'discount_amount': float(best.discount_amount or 0),
        'end_date':        str(best.end_date) if best.end_date else None,
    }})


# ── Site CREATE / UPDATE ──────────────────────────────────
@manager_bp.route('/api/sites', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def create_site():
    d       = request.get_json()
    site_id = (d.get('site_id') or '').strip()
    if not site_id:
        return jsonify({'status': 'error', 'message': 'site_id is required'}), 400
    if Site.query.filter_by(site_id=site_id).first():
        return jsonify({'status': 'error', 'message': 'Site ID already exists'}), 400
    from datetime import date as _d
    s = Site(
        site_id     = site_id,
        site_name   = d.get('site_name', ''),
        site_format = d.get('site_format', ''),
        region      = d.get('region', ''),
        city        = d.get('city', ''),
        state_id    = d.get('state_id'),
        store_size  = int(d.get('store_size', 0) or 0),
        status      = d.get('status', 'Active'),
    )
    if d.get('open_date'):
        try: s.open_date = _d.fromisoformat(d['open_date'])
        except: pass
    db.session.add(s)
    db.session.commit()
    log_action('CREATE', 'Sites', f'Site {site_id}', f'{s.site_name}, {s.city}')
    return jsonify({'status': 'success', 'site_id': site_id})


@manager_bp.route('/api/sites/<site_id>', methods=['PUT'])
@login_required
@role_required('manager')
@handle_errors
def update_site(site_id):
    s = Site.query.filter_by(site_id=site_id).first()
    if not s:
        return jsonify({'status': 'error', 'message': 'Site not found'}), 404
    d = request.get_json()
    if 'site_name'   in d: s.site_name   = d['site_name']
    if 'site_format' in d: s.site_format = d['site_format']
    if 'region'      in d: s.region      = d['region']
    if 'city'        in d: s.city        = d['city']
    if 'state_id'    in d: s.state_id    = d['state_id']
    if 'store_size'  in d: s.store_size  = int(d['store_size'] or 0)
    if 'status'      in d: s.status      = d['status']
    db.session.commit()
    log_action('UPDATE', 'Sites', f'Site {site_id}', f'Updated: {list(d.keys())}')
    return jsonify({'status': 'success'})


# ── Customer CREATE ───────────────────────────────────────
@manager_bp.route('/api/customers', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def list_customers():
    q = request.args.get('q', '').strip()
    query = Customer.query
    if q:
        query = query.filter(Customer.customer_id.ilike(f'%{q}%'))
    customers = query.order_by(Customer.customer_id).limit(200).all()
    return jsonify({'customers': [{'customer_id': c.customer_id} for c in customers]})


@manager_bp.route('/api/customers', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def create_customer():
    d           = request.get_json()
    customer_id = (d.get('customer_id') or '').strip()
    if not customer_id:
        count       = Customer.query.count()
        customer_id = f'CUST{10000 + count + 1}'
    if Customer.query.filter_by(customer_id=customer_id).first():
        return jsonify({'status': 'error', 'message': 'Customer ID already exists'}), 400
    from datetime import date as _d
    c = Customer(
        customer_id        = customer_id,
        age                = int(d.get('age', 0) or 0),
        gender             = d.get('gender', ''),
        income_bracket     = d.get('income_bracket', ''),
        purchase_frequency = int(d.get('purchase_frequency', 0) or 0),
        average_spend      = float(d.get('average_spend', 0) or 0),
        preferred_categories = d.get('preferred_categories', ''),
        total_spend        = float(d.get('total_spend', 0) or 0),
        clv                = float(d.get('clv', 0) or 0),
        csat               = float(d.get('csat', 0) or 0),
        nps                = int(d.get('nps', 0) or 0),
    )
    if d.get('last_purchase_date'):
        try: c.last_purchase_date = _d.fromisoformat(d['last_purchase_date'])
        except: pass
    db.session.add(c)
    db.session.commit()
    log_action('CREATE', 'Customers', f'Customer {customer_id}', '')
    return jsonify({'status': 'success', 'customer_id': customer_id, 'customer': c.to_dict()})


# ── Category CREATE / UPDATE / DELETE (manager access) ────
@manager_bp.route('/api/categories', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def create_category_manager():
    d = request.get_json()
    cat_name = (d.get('category_name') or '').strip()
    sub_name = (d.get('subcategory_name') or '').strip()
    if not cat_name:
        return jsonify({'status': 'error', 'message': 'Category name is required'}), 400
    cat = Category.query.filter_by(category_name=cat_name).first()
    if not cat:
        cat = Category(category_name=cat_name)
        db.session.add(cat)
        db.session.flush()
    if sub_name:
        if not Subcategory.query.filter_by(category_id=cat.id, subcategory_name=sub_name).first():
            db.session.add(Subcategory(category_id=cat.id, subcategory_name=sub_name))
    db.session.commit()
    log_action('CREATE', 'Categories', f'Category {cat_name}', f'Subcategory: {sub_name}')
    return jsonify({'status': 'success', 'category': cat.to_dict()})


@manager_bp.route('/api/categories/<int:cat_id>', methods=['PUT'])
@login_required
@role_required('manager')
@handle_errors
def update_category_manager(cat_id):
    cat = db.session.get(Category, cat_id)
    if not cat:
        return jsonify({'status': 'error', 'message': 'Category not found'}), 404
    d        = request.get_json()
    new_name = (d.get('category_name') or '').strip()
    if not new_name:
        return jsonify({'status': 'error', 'message': 'Category name is required'}), 400
    old_name          = cat.category_name
    cat.category_name = new_name
    db.session.commit()
    log_action('UPDATE', 'Categories', f'Category {old_name}', f'Renamed to {new_name}')
    return jsonify({'status': 'success', 'category': cat.to_dict()})


@manager_bp.route('/api/categories/<int:cat_id>', methods=['DELETE'])
@login_required
@role_required('manager')
@handle_errors
def delete_category_manager(cat_id):
    cat = db.session.get(Category, cat_id)
    if not cat:
        return jsonify({'status': 'error', 'message': 'Category not found'}), 404
    name = cat.category_name
    db.session.delete(cat)
    db.session.commit()
    log_action('DELETE', 'Categories', f'Category {name}', f'ID: {cat_id}')
    return jsonify({'status': 'success'})


# ── Product toggle status (manager) ──────────────────────
@manager_bp.route('/api/products/<product_id>/toggle-status', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def toggle_product_status_manager(product_id):
    p = Product.query.filter_by(product_id=product_id).first()
    if not p:
        return jsonify({'status': 'error', 'message': 'Product not found'}), 404
    p.status = 'Inactive' if (p.status or 'Active') == 'Active' else 'Active'
    db.session.commit()
    log_action('UPDATE', 'Products', f'Product {product_id}', f'Status → {p.status}')
    return jsonify({'status': 'success', 'new_status': p.status})


# ── Next SKU helper ───────────────────────────────────────
@manager_bp.route('/api/products/next-sku', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def next_sku():
    """Return the next available auto-generated product SKU."""
    last_id = db.session.query(func.max(Product.id)).scalar() or 0
    return jsonify({'sku': f'PRD{10000 + last_id + 1}'})


@manager_bp.route('/api/products/validate-sku', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def validate_sku():
    sku = request.args.get('sku', '').strip()
    if not sku:
        return jsonify({'available': False, 'message': 'SKU is required'}), 400
    exists = Product.query.filter_by(product_id=sku).first() is not None
    return jsonify({'available': not exists, 'sku': sku})


# ── Promotions (view-only) ────────────────────────────────
@manager_bp.route('/promotions')
@login_required
@role_required('manager')
@handle_errors
def promotions_page():
    return render_template('manager/promotions.html')


# ── Seasonal Planning (view-only) ─────────────────────────
@manager_bp.route('/seasonal-plan')
@login_required
@role_required('manager')
@handle_errors
def seasonal_plan_page():
    return render_template('manager/seasonal_plan.html')


# ══════════════════════════════════════════════════════════════
# SEASONAL PLANS — Manager Full CRUD (scoped to manager site)
# ══════════════════════════════════════════════════════════════
@manager_bp.route('/api/seasonal-plans', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def manager_seasonal_plans_list():
    site_id  = _manager_site_id()
    page     = request.args.get('page', 1, type=int)
    q        = request.args.get('q', '').strip()
    per_page = 20
    query    = (db.session.query(SeasonalPlan, Site)
                .join(Site, SeasonalPlan.site_id == Site.site_id, isouter=True))
    if site_id:
        query = query.filter(SeasonalPlan.site_id == site_id)
    if q:
        query = query.filter(
            (SeasonalPlan.month.ilike(f'%{q}%')) |
            (SeasonalPlan.product_category.ilike(f'%{q}%'))
        )
    total   = query.count()
    records = query.order_by(SeasonalPlan.id.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'records': [{
            'id':              sp.id,
            'month':           sp.month,
            'site_id':         sp.site_id,
            'site_name':       s.site_name if s else (sp.site_id or 'All Sites'),
            'category':        sp.product_category,
            'forecasted_sales':float(sp.forecasted_sales or 0),
            'actual_sales':    float(sp.actual_sales or 0),
            'seasonal_adj':    float(sp.seasonal_adjustments or 0),
        } for sp, s in records],
        'total': total, 'page': page, 'per_page': per_page,
    })


@manager_bp.route('/api/seasonal-plans', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def manager_seasonal_plans_create():
    d     = request.get_json()
    month = (d.get('month') or '').strip()
    if not month:
        return jsonify({'status': 'error', 'message': 'Month is required'}), 400
    site_id = d.get('site_id') or _manager_site_id() or ''
    sp = SeasonalPlan(
        month                = month,
        site_id              = site_id,
        product_category     = d.get('category', ''),
        forecasted_sales     = float(d.get('forecasted_sales', 0) or 0),
        actual_sales         = float(d.get('actual_sales', 0) or 0),
        seasonal_adjustments = float(d.get('seasonal_adj', 0) or 0),
    )
    db.session.add(sp)
    db.session.commit()
    log_action('CREATE', 'SeasonalPlan', f'{month} / {site_id}', 'Manager created')
    return jsonify({'status': 'success', 'id': sp.id})


@manager_bp.route('/api/seasonal-plans/<int:sp_id>', methods=['PUT'])
@login_required
@role_required('manager')
@handle_errors
def manager_seasonal_plans_update(sp_id):
    sp = db.session.get(SeasonalPlan, sp_id)
    if not sp:
        return jsonify({'status': 'error', 'message': 'Plan not found'}), 404
    d = request.get_json()
    if 'month'            in d: sp.month                = d['month']
    if 'site_id'          in d: sp.site_id              = d['site_id']
    if 'category'         in d: sp.product_category     = d['category']
    if 'forecasted_sales' in d: sp.forecasted_sales     = float(d['forecasted_sales'] or 0)
    if 'actual_sales'     in d: sp.actual_sales         = float(d['actual_sales'] or 0)
    if 'seasonal_adj'     in d: sp.seasonal_adjustments = float(d['seasonal_adj'] or 0)
    db.session.commit()
    return jsonify({'status': 'success'})


@manager_bp.route('/api/seasonal-plans/<int:sp_id>', methods=['DELETE'])
@login_required
@role_required('manager')
@handle_errors
def manager_seasonal_plans_delete(sp_id):
    sp = db.session.get(SeasonalPlan, sp_id)
    if not sp:
        return jsonify({'status': 'error', 'message': 'Plan not found'}), 404
    db.session.delete(sp)
    db.session.commit()
    log_action('DELETE', 'SeasonalPlan', f'ID {sp_id}', 'Manager deleted')
    return jsonify({'status': 'success'})


# ─── INVOICE GENERATION ──────────────────────────────────────────────────────

@manager_bp.route('/invoice/so/<so_number>')
@login_required
@role_required('manager')
@handle_errors
def generate_so_invoice_mgr(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return "Sales Order not found", 404
    so_dict = so.to_dict()
    site_obj = Site.query.filter_by(site_id=so.site).first()
    site_info = {'site_id': so.site, 'site_name': '', 'city': '', 'region': ''}
    if site_obj:
        site_info = {'site_id': site_obj.site_id, 'site_name': site_obj.site_name or '', 'city': site_obj.city or '', 'region': site_obj.region or ''}
    cust_info = {'customer_id': so.customer_id, 'name': so.customer, 'email': so.customer_email, 'state': so.state}
    inv_number = f"INV-SO-{so_number}"
    import datetime
    generated_date = datetime.date.today().strftime("%d %b %Y")
    return render_template('invoice.html',
        invoice_type='SALES INVOICE',
        inv_number=inv_number,
        order_ref=so_number,
        generated_date=generated_date,
        order_date=so.created_at[:10] if so.created_at else '',
        shipped_date=so.dispatched_at[:10] if so.dispatched_at else '',
        status=so.status,
        bill_to=cust_info,
        warehouse=site_info,
        items=so_dict.get('items', []),
        subtotal=so.total_amount,
        gst_rate=18,
        discount=0,
        notes=so.notes or '',
        dispatch_type=so.dispatch_type or '',
    )

@manager_bp.route('/invoice/po/<po_number>')
@login_required
@role_required('manager')
@handle_errors
def generate_po_invoice_mgr(po_number):
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return "Purchase Order not found", 404
    site_raw = po.site or ''
    site_id = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()
    site_obj = Site.query.filter_by(site_id=site_id).first()
    site_info = {'site_id': site_id, 'site_name': '', 'city': '', 'region': ''}
    if site_obj:
        site_info = {'site_id': site_obj.site_id, 'site_name': site_obj.site_name or '', 'city': site_obj.city or '', 'region': site_obj.region or ''}
    sup_name = po.supplier or '—'
    sup_email = ''
    if po.supplier_rel:
        sup_name = po.supplier_rel.supplier_name
        sup_email = po.supplier_rel.email or ''
    supplier_info = {'name': sup_name, 'email': sup_email, 'id': po.supplier_id}
    items = [{'product_name': po.product_name, 'product_id': po.product_id, 'quantity': po.quantity, 'unit_price': po.unit_cost, 'amount': po.total_cost}]
    inv_number = f"INV-PO-{po_number}"
    import datetime
    generated_date = datetime.date.today().strftime("%d %b %Y")
    return render_template('invoice.html',
        invoice_type='PURCHASE ORDER',
        inv_number=inv_number,
        order_ref=po_number,
        generated_date=generated_date,
        order_date=po.created_at[:10] if po.created_at else '',
        shipped_date=po.received_at[:10] if po.received_at else '',
        status=po.status,
        bill_to=supplier_info,
        is_purchase=True,
        warehouse=site_info,
        items=items,
        subtotal=po.total_cost,
        gst_rate=18,
        discount=0,
        notes=po.notes or '',
        dispatch_type='',
    )


# ═══════════════════════════════════════════════════════════
# ── SALES RETURNS (Manager) ─────────────────────────────────
# ═══════════════════════════════════════════════════════════

@manager_bp.route('/sales-returns')
@login_required
@role_required('manager')
def sales_returns_page():
    return render_template('manager/sales_returns.html')


@manager_bp.route('/api/sales-returns', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def mgr_get_sales_returns():
    q        = request.args.get('q', '').strip().lower()
    status   = request.args.get('status', '').strip()
    page     = request.args.get('page', 1, type=int)
    per_page = 20
    query    = SalesReturn.query.filter_by(role='manager')
    if status:
        query = query.filter_by(status=status)
    if q:
        query = query.filter(
            db.or_(
                SalesReturn.return_number.ilike(f'%{q}%'),
                SalesReturn.so_number.ilike(f'%{q}%'),
                SalesReturn.customer.ilike(f'%{q}%'),
            )
        )
    all_records     = query.all()
    total           = len(all_records)
    pending_count   = sum(1 for r in all_records if r.status == 'Pending')
    approved_count  = sum(1 for r in all_records if r.status == 'Approved')
    rejected_count  = sum(1 for r in all_records if r.status == 'Rejected')
    total_refund    = sum(float(r.total_refund or 0) for r in all_records)
    records         = all_records[(page - 1) * per_page: page * per_page]
    return jsonify({
        'returns': [r.to_dict() for r in records],
        'total':   total,
        'page':    page,
        'stats': {
            'total_returns': total,
            'pending':       pending_count,
            'approved':      approved_count,
            'rejected':      rejected_count,
            'total_refund':  round(total_refund, 2),
        }
    })


@manager_bp.route('/api/sales-returns', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def mgr_create_sales_return():
    from datetime import date as _date
    d      = request.get_json()
    so_num = (d.get('so_number') or '').strip()
    if not so_num:
        return jsonify({'status': 'error', 'message': 'SO Number is required'}), 400
    so = SalesOrder.query.filter_by(so_number=so_num).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'Sales Order not found'}), 404
    rn     = 'SR-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    items  = d.get('items', [])
    refund = sum(float(i.get('unit_price', 0)) * int(i.get('quantity', 0)) for i in items)
    ret = SalesReturn(
        return_number = rn,
        so_number     = so_num,
        customer      = so.customer or d.get('customer', ''),
        site          = so.site or '',
        return_reason = d.get('return_reason', ''),
        items_json    = json.dumps(items),
        total_refund  = round(refund, 2),
        status        = 'Pending',
        notes         = d.get('notes', ''),
        created_at    = str(_date.today()),
        created_by    = session.get('username', 'Manager'),
        role          = 'manager',
    )
    db.session.add(ret)
    db.session.commit()
    log_action('CREATE', 'Sales Returns', f'Return {rn}', f'SO: {so_num}, Refund: {refund:.2f}')
    return jsonify({'status': 'success', 'return_number': rn})


@manager_bp.route('/api/sales-returns/<rn>/approve', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def mgr_approve_sales_return(rn):
    from datetime import date as _date
    ret = SalesReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status      = 'Approved'
    ret.approved_at = str(_date.today())
    ret.approved_by = session.get('username', 'Manager')
    db.session.commit()
    log_action('UPDATE', 'Sales Returns', f'Return {rn}', 'Status: Approved')
    return jsonify({'status': 'success'})


@manager_bp.route('/api/sales-returns/<rn>/reject', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def mgr_reject_sales_return(rn):
    ret = SalesReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status = 'Rejected'
    db.session.commit()
    log_action('UPDATE', 'Sales Returns', f'Return {rn}', 'Status: Rejected')
    return jsonify({'status': 'success'})


# ═══════════════════════════════════════════════════════════
# ── PURCHASE RETURNS (Manager) ───────────────────────────────
# ═══════════════════════════════════════════════════════════

@manager_bp.route('/purchase-returns')
@login_required
@role_required('manager')
def purchase_returns_page():
    return render_template('manager/purchase_returns.html')


@manager_bp.route('/api/purchase-returns', methods=['GET'])
@login_required
@role_required('manager')
@handle_errors
def mgr_get_purchase_returns():
    q        = request.args.get('q', '').strip().lower()
    status   = request.args.get('status', '').strip()
    page     = request.args.get('page', 1, type=int)
    per_page = 20
    query    = PurchaseReturn.query.filter_by(role='manager')
    if status:
        query = query.filter_by(status=status)
    if q:
        query = query.filter(
            db.or_(
                PurchaseReturn.return_number.ilike(f'%{q}%'),
                PurchaseReturn.po_number.ilike(f'%{q}%'),
                PurchaseReturn.supplier.ilike(f'%{q}%'),
            )
        )
    all_records    = query.all()
    total          = len(all_records)
    pending_count  = sum(1 for r in all_records if r.status == 'Pending')
    approved_count = sum(1 for r in all_records if r.status == 'Approved')
    total_credit   = sum(float(r.total_credit or 0) for r in all_records)
    records        = all_records[(page - 1) * per_page: page * per_page]
    return jsonify({
        'returns': [r.to_dict() for r in records],
        'total':   total,
        'page':    page,
        'stats': {
            'total_returns': total,
            'pending':       pending_count,
            'approved':      approved_count,
            'total_credit':  round(total_credit, 2),
        }
    })


@manager_bp.route('/api/purchase-returns', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def mgr_create_purchase_return():
    from datetime import date as _date
    d      = request.get_json()
    po_num = (d.get('po_number') or '').strip()
    if not po_num:
        return jsonify({'status': 'error', 'message': 'PO Number is required'}), 400
    po = PurchaseOrder.query.filter_by(po_number=po_num).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Purchase Order not found'}), 404
    rn        = 'PR-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    qty       = int(d.get('quantity', 0))
    unit_cost = float(d.get('unit_cost', po.unit_cost or 0))
    credit    = round(qty * unit_cost, 2)
    ret = PurchaseReturn(
        return_number = rn,
        po_number     = po_num,
        supplier      = po.supplier or '',
        site          = po.site or '',
        return_reason = d.get('return_reason', ''),
        product_name  = po.product_name or d.get('product_name', ''),
        product_id    = po.product_id or '',
        quantity      = qty,
        unit_cost     = unit_cost,
        total_credit  = credit,
        status        = 'Pending',
        notes         = d.get('notes', ''),
        created_at    = str(_date.today()),
        created_by    = session.get('username', 'Manager'),
        role          = 'manager',
    )
    db.session.add(ret)
    db.session.commit()
    log_action('CREATE', 'Purchase Returns', f'Return {rn}', f'PO: {po_num}, Credit: {credit:.2f}')
    return jsonify({'status': 'success', 'return_number': rn})


@manager_bp.route('/api/purchase-returns/<rn>/approve', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def mgr_approve_purchase_return(rn):
    from datetime import date as _date
    ret = PurchaseReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status      = 'Approved'
    ret.approved_at = str(_date.today())
    ret.approved_by = session.get('username', 'Manager')
    db.session.commit()
    log_action('UPDATE', 'Purchase Returns', f'Return {rn}', 'Status: Approved')
    return jsonify({'status': 'success'})


@manager_bp.route('/api/purchase-returns/<rn>/reject', methods=['POST'])
@login_required
@role_required('manager')
@handle_errors
def mgr_reject_purchase_return(rn):
    ret = PurchaseReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status = 'Rejected'
    db.session.commit()
    log_action('UPDATE', 'Purchase Returns', f'Return {rn}', 'Status: Rejected')
    return jsonify({'status': 'success'})
