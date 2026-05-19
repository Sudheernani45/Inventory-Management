"""
analyst_routes.py — routes for the Analyst role.
Analyst permissions:
  Dashboard : view analytics, charts, KPIs (read-only)
  Products  : view only
  Inventory : view only
  Sales     : view only (all sites)
  Shipments : view only
  Promotions: view only
"""
from flask import Blueprint, render_template, session, jsonify, request
from models.db import db
from models.records import Site, Inventory, Sale, Product, Logistics, Promotion, SeasonalPlan, Customer, Supplier, SalesOrder, PurchaseOrder, AuditLog, SalesReturn, PurchaseReturn
from routes.auth_routes import login_required, role_required, handle_errors
from sqlalchemy import func
import calendar

analyst_bp = Blueprint('analyst', __name__)


# ═══════════════════════════════════════════════════════════
#  PAGE ROUTES
# ═══════════════════════════════════════════════════════════

@analyst_bp.route('/dashboard')
@login_required
@role_required('analyst')
@handle_errors
def dashboard():
    return render_template('analyst/dashboard.html')


@analyst_bp.route('/products')
@login_required
@role_required('analyst')
@handle_errors
def products():
    return render_template('analyst/products.html')




# ── Dashboard: Monthly Metrics ───────────────────────────
@analyst_bp.route('/api/monthly-metrics')
@login_required
@role_required('analyst')
@handle_errors
def analyst_monthly_metrics():
    from sqlalchemy import func
    rows = db.session.query(
        func.to_char(Sale.date, 'YYYY-MM').label('month'),
        func.sum(Sale.units_sold).label('units_sold'),
        func.sum(Sale.revenue).label('revenue'),
    ).group_by(func.to_char(Sale.date, 'YYYY-MM')).order_by('month').all()
    profit_rows = db.session.query(
        func.to_char(Sale.date, 'YYYY-MM').label('month'),
        func.sum((Sale.revenue - Sale.discounts) - Sale.units_sold * Product.unit_cost).label('profit')
    ).join(Product, Sale.product_id == Product.product_id, isouter=True).group_by(
        func.to_char(Sale.date, 'YYYY-MM')
    ).all()
    profit_map = {r.month: round(float(r.profit or 0), 2) for r in profit_rows}
    po_rows = db.session.query(
        PurchaseOrder.created_at, func.sum(PurchaseOrder.quantity).label('qty')
    ).filter(PurchaseOrder.status == 'Approved').group_by(PurchaseOrder.created_at).all()
    replen_map = {}
    for rr in po_rows:
        if rr.created_at and len(rr.created_at) >= 7:
            mk = rr.created_at[:7]
            replen_map[mk] = replen_map.get(mk, 0) + int(rr.qty or 0)
    months = [r.month for r in rows if r.month][-12:]
    return jsonify({
        'labels':        months,
        'units_sold':    [int(next((r.units_sold or 0 for r in rows if r.month == m), 0)) for m in months],
        'profit':        [profit_map.get(m, 0) for m in months],
        'replenishment': [replen_map.get(m, 0) for m in months],
    })


# ── Dashboard: Customer Stats ────────────────────────────
@analyst_bp.route('/api/customer-stats')
@login_required
@role_required('analyst')
@handle_errors
def analyst_customer_stats():
    from sqlalchemy import func
    total    = Customer.query.count()
    avg_spend= float(db.session.query(func.avg(Customer.average_spend)).scalar() or 0)
    avg_clv  = float(db.session.query(func.avg(Customer.clv)).scalar() or 0)
    return jsonify({'total': total, 'avg_spend': avg_spend, 'avg_clv': avg_clv})


# ── Dashboard: Purchase Orders Summary ──────────────────
@analyst_bp.route('/api/purchase-orders/summary')
@login_required
@role_required('analyst')
@handle_errors
def analyst_po_summary():
    from sqlalchemy import func
    total = PurchaseOrder.query.count()
    return jsonify({'total': total})

@analyst_bp.route('/inventory')
@login_required
@role_required('analyst')
@handle_errors
def inventory():
    return render_template('analyst/inventory.html')


@analyst_bp.route('/sales')
@login_required
@role_required('analyst')
@handle_errors
def sales():
    return render_template('analyst/sales.html')


@analyst_bp.route('/shipments')
@login_required
@role_required('analyst')
@handle_errors
def shipments():
    return render_template('analyst/shipments.html')


@analyst_bp.route('/sites')
@login_required
@role_required('analyst')
@handle_errors
def sites():
    return render_template('analyst/sites.html')


@analyst_bp.route('/customers')
@login_required
@role_required('analyst')
@handle_errors
def customers():
    return render_template('analyst/customers.html')


@analyst_bp.route('/suppliers')
@login_required
@role_required('analyst')
@handle_errors
def suppliers():
    return render_template('analyst/suppliers.html')


@analyst_bp.route('/sales-orders')
@login_required
@role_required('analyst')
@handle_errors
def sales_orders():
    return render_template('analyst/sales_orders.html')


@analyst_bp.route('/purchase-orders')
@login_required
@role_required('analyst')
@handle_errors
def purchase_orders():
    return render_template('analyst/purchase_orders.html')


@analyst_bp.route('/audit-log')
@login_required
@role_required('analyst')
@handle_errors
def audit_log():
    return render_template('analyst/audit_log.html')


@analyst_bp.route('/promotions')
@login_required
@role_required('analyst')
@handle_errors
def promotions():
    return render_template('analyst/promotions.html')


@analyst_bp.route('/seasonal-plan')
@login_required
@role_required('analyst')
@handle_errors
def seasonal_plan():
    return render_template('analyst/seasonal_plan.html')


# ═══════════════════════════════════════════════════════════
#  JSON API
# ═══════════════════════════════════════════════════════════

@analyst_bp.route('/api/stats')
@login_required
@role_required('analyst')
@handle_errors
def analyst_stats():
    total_revenue  = float(db.session.query(func.sum(Sale.revenue)).scalar() or 0)
    units_sold     = int(db.session.query(func.sum(Sale.units_sold)).scalar() or 0)
    stockout_count = Inventory.query.filter_by(stockout_flag='Yes').count()
    total_products = Product.query.count()
    active_sites   = Site.query.filter_by(status='Active').count()
    total_returns  = int(db.session.query(func.sum(Sale.returns)).scalar() or 0)
    total_discounts= float(db.session.query(func.sum(Sale.discounts)).scalar() or 0)
    low_stock      = Inventory.query.filter(
        Inventory.ending_inventory > 0,
        Inventory.ending_inventory <= 10
    ).count()
    return jsonify({
        'total_revenue':   total_revenue,
        'units_sold':      units_sold,
        'stockout_count':  stockout_count,
        'total_products':  total_products,
        'active_sites':    active_sites,
        'total_returns':   total_returns,
        'total_discounts': total_discounts,
        'low_stock':       low_stock,
    })


@analyst_bp.route('/api/revenue-trend')
@login_required
@role_required('analyst')
@handle_errors
def revenue_trend():
    rows = (db.session.query(
                func.to_char(Sale.date, 'YYYY-MM').label('month'),
                func.sum(Sale.revenue).label('rev'),
                func.sum(Sale.units_sold).label('units'))
            .group_by('month')
            .order_by('month')
            .limit(12).all())
    labels, revenue, units = [], [], []
    for r in rows:
        if r.month:
            try:
                y, m = r.month.split('-')
                labels.append(f"{calendar.month_abbr[int(m)]}-{y}")
            except Exception:
                labels.append(r.month)
        else:
            labels.append('—')
        revenue.append(float(r.rev or 0))
        units.append(int(r.units or 0))
    return jsonify({'labels': labels, 'revenue': revenue, 'units': units})


@analyst_bp.route('/api/category-revenue')
@login_required
@role_required('analyst')
@handle_errors
def category_revenue():
    rows = (db.session.query(
                Product.category,
                func.sum(Sale.revenue).label('rev'),
                func.sum(Sale.units_sold).label('units'))
            .join(Sale, Sale.product_id == Product.product_id, isouter=True)
            .group_by(Product.category)
            .order_by(func.sum(Sale.revenue).desc())
            .limit(8).all())
    return jsonify({
        'labels': [r.category or 'Unknown' for r in rows],
        'revenue': [float(r.rev or 0) for r in rows],
        'units':   [int(r.units or 0) for r in rows],
    })


@analyst_bp.route('/api/site-performance')
@login_required
@role_required('analyst')
@handle_errors
def site_performance():
    rows = (db.session.query(
                Site.site_name,
                Site.site_id,
                func.sum(Sale.revenue).label('rev'),
                func.sum(Sale.units_sold).label('units'))
            .join(Sale, Sale.site_id == Site.site_id, isouter=True)
            .group_by(Site.site_id)
            .order_by(func.sum(Sale.revenue).desc())
            .limit(10).all())
    return jsonify({
        'sites': [{'site': r.site_name or r.site_id, 'revenue': float(r.rev or 0), 'units': int(r.units or 0)} for r in rows]
    })


@analyst_bp.route('/api/stockout-sites')
@login_required
@role_required('analyst')
@handle_errors
def stockout_sites():
    rows = (db.session.query(
                Site.site_name,
                func.count(Inventory.id).label('cnt'))
            .join(Inventory, Inventory.site_id == Site.site_id, isouter=True)
            .filter(Inventory.stockout_flag == 'Yes')
            .group_by(Site.site_id)
            .order_by(func.count(Inventory.id).desc())
            .limit(8).all())
    return jsonify({'labels': [r.site_name for r in rows], 'values': [r.cnt for r in rows]})


@analyst_bp.route('/api/products')
@login_required
@role_required('analyst')
@handle_errors
def api_products():
    page  = request.args.get('page', 1, type=int)
    q     = request.args.get('q', '').strip()
    per_page = 20
    query = Product.query
    if q:
        query = query.filter(Product.product_name.ilike(f'%{q}%'))
    total = query.count()
    items = query.order_by(Product.product_id).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'products': [{'product_id': p.product_id, 'product_name': p.product_name,
                      'category': p.category, 'subcategory': p.subcategory,
                      'unit_cost': float(p.unit_cost or 0), 'unit_price': float(p.unit_price or 0),
                      'supplier': p.supplier} for p in items],
        'total': total, 'page': page, 'per_page': per_page,
    })


@analyst_bp.route('/api/inventory')
@login_required
@role_required('analyst')
@handle_errors
def api_inventory():
    page     = request.args.get('page', 1, type=int)
    stockout = request.args.get('stockout', '').strip()
    site_f   = request.args.get('site_id', '').strip()
    per_page = 20
    query = (db.session.query(Inventory, Product, Site)
             .join(Product, Inventory.product_id == Product.product_id, isouter=True)
             .join(Site, Inventory.site_id == Site.site_id, isouter=True))
    if stockout == 'yes':
        query = query.filter(Inventory.stockout_flag == 'Yes')
    if site_f:
        query = query.filter(Inventory.site_id == site_f)
    total = query.count()
    rows  = query.order_by(Inventory.id.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'records': [{'product_id': inv.product_id, 'product_name': p.product_name if p else None,
                     'site_id': inv.site_id, 'site_name': s.site_name if s else None,
                     'beginning': inv.beginning_inventory, 'ending': inv.ending_inventory,
                     'stockout': inv.stockout_flag} for inv, p, s in rows],
        'total': total, 'page': page, 'per_page': per_page,
    })


@analyst_bp.route('/api/sales')
@login_required
@role_required('analyst')
@handle_errors
def api_sales():
    page   = request.args.get('page', 1, type=int)
    site_f = request.args.get('site_id', '').strip()
    per_page = 20
    query = (db.session.query(Sale, Product, Site)
             .join(Product, Sale.product_id == Product.product_id, isouter=True)
             .join(Site, Sale.site_id == Site.site_id, isouter=True))
    if site_f:
        query = query.filter(Sale.site_id == site_f)
    total = query.count()
    rows  = query.order_by(Sale.date.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'records': [{'date': str(sale.date) if sale.date else None,
                     'product': p.product_name if p else sale.product_id,
                     'site': s.site_name if s else sale.site_id,
                     'units_sold': sale.units_sold, 'revenue': float(sale.revenue or 0),
                     'discounts': float(sale.discounts or 0), 'returns': sale.returns} for sale, p, s in rows],
        'total': total, 'page': page, 'per_page': per_page,
    })


@analyst_bp.route('/api/shipments/stats')
@login_required
@role_required('analyst')
@handle_errors
def analyst_shipments_stats():
    from sqlalchemy import func as sqlfunc
    rows = db.session.query(Logistics.delivery_status, sqlfunc.count(Logistics.id)).group_by(Logistics.delivery_status).all()
    counts = {s: cnt for s, cnt in rows}
    return jsonify({'total': sum(counts.values()), 'by_status': counts,
                    'in_transit': counts.get('In Transit',0), 'delivered': counts.get('Delivered',0),
                    'pending': counts.get('Pending',0), 'delayed': counts.get('Delayed',0),
                    'cancelled': counts.get('Cancelled',0), 'dispatched': counts.get('Dispatched',0),
                    'picked_up': counts.get('Picked Up',0), 'out_for_delivery': counts.get('Out for Delivery',0)})


@analyst_bp.route('/api/shipments')
@analyst_bp.route('/api/shipments/list')
@login_required
@role_required('analyst')
@handle_errors
def api_shipments():
    from sqlalchemy import func as sqlfunc
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status   = request.args.get('status', '').strip()
    ttype    = request.args.get('ttype', '').strip()
    q_str    = request.args.get('q', '').strip()
    query = (db.session.query(Logistics, Product, Site)
             .join(Product, Logistics.product_id == Product.product_id, isouter=True)
             .join(Site, Logistics.site_id == Site.site_id, isouter=True))
    if status:
        query = query.filter(Logistics.delivery_status == status)
    if ttype:
        query = query.filter(Logistics.transportation_type == ttype)
    if q_str:
        query = query.filter(db.or_(
            Product.product_name.ilike(f'%{q_str}%'),
            Logistics.shipment_id.ilike(f'%{q_str}%'),
            Site.site_name.ilike(f'%{q_str}%'),
        ))
    total = query.with_entities(sqlfunc.count(Logistics.id)).scalar()
    rows  = query.order_by(Logistics.shipment_date.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'records': [{'shipment_id': l.shipment_id,
                     'product': p.product_name if p else l.product_id,
                     'site': s.site_name if s else l.site_id,
                     'date': str(l.shipment_date) if l.shipment_date else None,
                     'quantity': l.quantity, 'status': l.delivery_status,
                     'transport': l.transportation_type} for l, p, s in rows],
        'total': total, 'page': page, 'per_page': per_page,
    })


@analyst_bp.route('/api/seasonal-plan')
@login_required
@role_required('analyst')
@handle_errors
def api_seasonal_plan():
    records = SeasonalPlan.query.order_by(SeasonalPlan.month).all()
    return jsonify({
        'records': [{'month': r.month, 'site_id': r.site_id, 'category': r.product_category,
                     'forecasted': float(r.forecasted_sales or 0), 'actual': float(r.actual_sales or 0),
                     'adjustment': float(r.seasonal_adjustments or 0)} for r in records]
    })


# ── Alias routes for new template naming ─────────────────

@analyst_bp.route('/api/sales-data')
@login_required
@role_required('analyst')
@handle_errors
def sales_data_alias():
    from models.records import Site as _Site
    page   = request.args.get('page', 1, type=int)
    site_f = request.args.get('site_id', '').strip()
    PER    = 20
    q = (db.session.query(Sale, Product, _Site)
         .join(Product, Sale.product_id == Product.product_id, isouter=True)
         .join(_Site, Sale.site_id == _Site.site_id, isouter=True))
    if site_f:
        q = q.filter(Sale.site_id == site_f)
    total   = q.count()
    records = q.order_by(Sale.date.desc()).offset((page-1)*PER).limit(PER).all()
    sites   = _Site.query.order_by(_Site.site_name).all()
    return jsonify({
        'records': [{'date': str(s.date) if s.date else '', 'product': p.product_name if p else s.product_id,
                     'site': st.site_name if st else s.site_id, 'units_sold': s.units_sold,
                     'revenue': float(s.revenue or 0), 'discounts': float(s.discounts or 0), 'returns': s.returns}
                    for s, p, st in records],
        'total': total, 'page': page, 'per_page': PER,
        'sites': [{'site_id': s.site_id, 'site_name': s.site_name} for s in sites],
    })


@analyst_bp.route('/api/inventory-data')
@login_required
@role_required('analyst')
@handle_errors
def inventory_data_alias():
    from models.records import Site as _Site
    page   = request.args.get('page', 1, type=int)
    site_f = request.args.get('site_id', '').strip()
    PER    = 20
    q = (db.session.query(Inventory, Product, _Site)
         .join(Product, Inventory.product_id == Product.product_id, isouter=True)
         .join(_Site, Inventory.site_id == _Site.site_id, isouter=True))
    if site_f:
        q = q.filter(Inventory.site_id == site_f)
    total   = q.count()
    records = q.order_by(Inventory.id.desc()).offset((page-1)*PER).limit(PER).all()
    sites   = _Site.query.order_by(_Site.site_name).all()
    from models.records import StockLevel
    prod_ids_a = list({inv.product_id for inv,p,s in records})
    sl_rows_a  = StockLevel.query.filter(StockLevel.product_id.in_(prod_ids_a)).all()
    sl_map_a   = {(sl.site_id, sl.product_id): (sl.qty_on_hand or 0) for sl in sl_rows_a}
    result_a   = []
    for inv, p, s in records:
        bi   = inv.beginning_inventory or 0
        ei   = inv.ending_inventory    or 0
        rep  = inv.replenishment       or 0
        bi_d = (ei + rep) if (bi == 0 and rep > 0) else bi
        ei_d = ei if ei > 0 else max(0, bi_d + rep)
        csqty= sl_map_a.get((inv.site_id, inv.product_id), ei_d)
        result_a.append({
            'product':             p.product_name if p else inv.product_id,
            'product_id':          inv.product_id,
            'site':                s.site_name    if s else inv.site_id,
            'site_id':             inv.site_id,
            'begin_inv':           bi_d,
            'end_inv':             ei_d,
            'replenish':           rep,
            'stockout':            'Yes' if csqty == 0 else ('Yes' if inv.stockout_flag=='Yes' else 'No'),
            'current_stock':       int(csqty),
            'unit_cost':           float(p.unit_cost  or 0) if p else 0,
            'unit_price':          float(p.unit_price or 0) if p else 0,
            'category':            p.category    if p and hasattr(p,'category')    else '',
            'so_count':            0,
            'so_total':            0.0,
            'po_count':            0,
            'po_total':            0.0,
        })
    return jsonify({
        'records': result_a,
        'total': total, 'page': page, 'per_page': PER,
        'sites': [{'site_id': s.site_id, 'site_name': s.site_name} for s in sites],
    })


@analyst_bp.route('/api/promotions-data')
@login_required
@role_required('analyst')
@handle_errors
def promotions_data_alias():
    page  = request.args.get('page', 1, type=int)
    PER   = 20
    recs  = (db.session.query(Promotion, Product, Site)
             .join(Product, Promotion.product_id == Product.product_id, isouter=True)
             .join(Site, Promotion.site_id == Site.site_id, isouter=True)
             .order_by(Promotion.start_date.desc())
             .offset((page-1)*PER).limit(PER).all())
    total = Promotion.query.count()
    return jsonify({
        'records': [{'product': p.product_name if p else promo.product_id, 'site': s.site_name if s else promo.site_id,
                     'type': promo.discount_type, 'amount': float(promo.discount_amount or 0),
                     'start_date': str(promo.start_date) if promo.start_date else '',
                     'end_date': str(promo.end_date) if promo.end_date else ''}
                    for promo, p, s in recs],
        'total': total, 'page': page, 'per_page': PER,
    })


@analyst_bp.route('/api/seasonal-plan-data')
@login_required
@role_required('analyst')
@handle_errors
def seasonal_plan_data_alias():
    records = SeasonalPlan.query.order_by(SeasonalPlan.month).all()
    return jsonify([{'month': r.month, 'site_id': r.site_id, 'category': r.product_category,
                     'forecast': float(r.forecasted_sales or 0), 'actual': float(r.actual_sales or 0),
                     'adjustment': float(r.seasonal_adjustments or 0)} for r in records])


# ═══════════════════════════════════════════════════════════
#  ADDITIONAL READ-ONLY JSON APIs (for new analyst pages)
# ═══════════════════════════════════════════════════════════

@analyst_bp.route('/api/sites')
@login_required
@role_required('analyst')
@handle_errors
def api_sites():
    from models.records import Site as _Site
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    PER = 20
    query = _Site.query
    if q:
        query = query.filter(_Site.site_name.ilike(f'%{q}%'))
    total = query.count()
    items = query.order_by(_Site.site_id).offset((page-1)*PER).limit(PER).all()
    return jsonify({
        'records': [{'site_id': s.site_id, 'site_name': s.site_name,
                     'region': s.region, 'status': s.status,
                     'city': s.city, 'site_format': s.site_format} for s in items],
        'total': total, 'page': page, 'per_page': PER,
    })


@analyst_bp.route('/api/customers')
@login_required
@role_required('analyst')
@handle_errors
def api_customers():
    from models.records import Customer, Sale
    from sqlalchemy import func
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    PER = 20
    query = Customer.query
    if q:
        query = query.filter(Customer.customer_id.ilike(f'%{q}%'))
    total = query.count()
    items = query.order_by(Customer.customer_id).offset((page-1)*PER).limit(PER).all()

    # Build spend lookup from Sales table for current page customers
    cust_ids = [c.customer_id for c in items]
    spend_rows = db.session.query(
        Sale.customer_id,
        func.sum(Sale.revenue).label('total'),
        func.avg(Sale.revenue).label('avg'),
        func.count(Sale.id).label('freq')
    ).filter(Sale.customer_id.in_(cust_ids)).group_by(Sale.customer_id).all()
    spend_map = {r.customer_id: r for r in spend_rows}

    records = []
    for c in items:
        sr = spend_map.get(c.customer_id)
        total_spend = float(sr.total or 0) if sr else float(c.total_spend or 0)
        avg_spend   = float(sr.avg   or 0) if sr else float(c.average_spend or 0)
        freq        = int(sr.freq    or 0) if sr else int(c.purchase_frequency or 0)
        records.append({
            'customer_id': c.customer_id,
            'age': c.age,
            'gender': c.gender,
            'income_bracket': c.income_bracket,
            'purchase_frequency': freq,
            'average_spend': avg_spend,
            'total_spend': total_spend,
            'preferred_categories': c.preferred_categories,
            'last_purchase_date': str(c.last_purchase_date) if c.last_purchase_date else '',
        })
    return jsonify({'records': records, 'total': total, 'page': page, 'per_page': PER})


@analyst_bp.route('/api/suppliers')
@login_required
@role_required('analyst')
@handle_errors
def api_suppliers():
    from models.records import Supplier
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    PER = 20
    query = Supplier.query
    if q:
        query = query.filter(Supplier.supplier_name.ilike(f'%{q}%'))
    total = query.count()
    items = query.order_by(Supplier.supplier_id).offset((page-1)*PER).limit(PER).all()
    return jsonify({
        'records': [{'supplier_id': s.supplier_id, 'supplier_name': s.supplier_name,
                     'contact': s.contact_person, 'email': s.email,
                     'phone': s.phone, 'category': s.category, 'status': s.status} for s in items],
        'total': total, 'page': page, 'per_page': PER,
    })


@analyst_bp.route('/api/sales-orders')
@login_required
@role_required('analyst')
@handle_errors
def api_sales_orders():
    from models.records import SalesOrder
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    PER = 20
    query = SalesOrder.query
    if q:
        query = query.filter(SalesOrder.so_number.ilike(f'%{q}%'))
    total = query.count()
    items = query.order_by(SalesOrder.created_at.desc()).offset((page-1)*PER).limit(PER).all()
    return jsonify({
        'records': [{'so_number': o.so_number, 'customer': o.customer,
                     'customer_id': o.customer_id,
                     'created_at': o.created_at or '',
                     'status': o.status, 'total_amount': float(o.total_amount or 0),
                     'site': o.site, 'dispatch_type': o.dispatch_type} for o in items],
        'total': total, 'page': page, 'per_page': PER,
    })


@analyst_bp.route('/api/purchase-orders')
@login_required
@role_required('analyst')
@handle_errors
def api_purchase_orders():
    from models.records import PurchaseOrder
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    PER = 20
    query = PurchaseOrder.query
    if q:
        query = query.filter(PurchaseOrder.po_number.ilike(f'%{q}%'))
    total = query.count()
    items = query.order_by(PurchaseOrder.created_at.desc()).offset((page-1)*PER).limit(PER).all()
    return jsonify({
        'records': [{'po_number': o.po_number, 'supplier': o.supplier,
                     'product_name': o.product_name,
                     'quantity': o.quantity, 'unit_cost': float(o.unit_cost or 0),
                     'total_cost': float(o.total_cost or 0),
                     'created_at': o.created_at or '',
                     'status': o.status, 'site': o.site,
                     'expected_delivery': o.expected_delivery} for o in items],
        'total': total, 'page': page, 'per_page': PER,
    })


@analyst_bp.route('/api/audit-log')
@login_required
@role_required('analyst')
@handle_errors
def api_audit_log():
    from models.records import AuditLog
    page = request.args.get('page', 1, type=int)
    PER = 20
    total = AuditLog.query.count()
    items = AuditLog.query.order_by(AuditLog.timestamp.desc()).offset((page-1)*PER).limit(PER).all()
    return jsonify({
        'records': [{'id': a.id, 'user': a.user, 'action': a.action,
                     'module': a.module, 'resource': a.resource,
                     'detail': a.detail,
                     'timestamp': a.to_dict()['timestamp'] if a.timestamp else ''} for a in items],
        'total': total, 'page': page, 'per_page': PER,
    })


# ── Purchase Returns (view-only) ──────────────────────────────────────────────

@analyst_bp.route('/purchase-returns')
@login_required
@role_required('analyst')
def purchase_returns():
    return render_template('analyst/purchase_returns.html')


@analyst_bp.route('/api/purchase-returns')
@login_required
@role_required('analyst')
@handle_errors
def api_purchase_returns():
    page   = request.args.get('page', 1, type=int)
    q      = request.args.get('q', '').strip()
    status = request.args.get('status', '').strip()
    PER    = 20
    query  = PurchaseReturn.query
    if q:
        query = query.filter(
            db.or_(
                PurchaseReturn.po_number.ilike(f'%{q}%'),
                PurchaseReturn.supplier.ilike(f'%{q}%'),
                PurchaseReturn.return_number.ilike(f'%{q}%'),
            )
        )
    if status:
        query = query.filter(PurchaseReturn.status == status)
    total = query.count()
    items = query.order_by(PurchaseReturn.id.desc()).offset((page - 1) * PER).limit(PER).all()
    return jsonify({
        'returns': [r.to_dict() for r in items],
        'total':   total,
        'page':    page,
        'per_page': PER,
    })


# ── Sales Returns (view-only) ─────────────────────────────────────────────────

@analyst_bp.route('/sales-returns')
@login_required
@role_required('analyst')
def sales_returns():
    return render_template('analyst/sales_returns.html')


@analyst_bp.route('/api/sales-returns')
@login_required
@role_required('analyst')
@handle_errors
def api_sales_returns():
    page   = request.args.get('page', 1, type=int)
    q      = request.args.get('q', '').strip()
    status = request.args.get('status', '').strip()
    PER    = 20
    query  = SalesReturn.query
    if q:
        query = query.filter(
            db.or_(
                SalesReturn.so_number.ilike(f'%{q}%'),
                SalesReturn.customer.ilike(f'%{q}%'),
                SalesReturn.return_number.ilike(f'%{q}%'),
            )
        )
    if status:
        query = query.filter(SalesReturn.status == status)
    total = query.count()
    items = query.order_by(SalesReturn.id.desc()).offset((page - 1) * PER).limit(PER).all()
    return jsonify({
        'returns': [r.to_dict() for r in items],
        'total':   total,
        'page':    page,
        'per_page': PER,
    })
