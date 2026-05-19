"""
api_routes.py  –  JSON API endpoints consumed by async/await JS frontend
"""
from flask import Blueprint, jsonify, request, session
from models.db import db
from models.user import User
from models.managers import Manager
from models.records import (Product, Site, Inventory, Logistics, Sale,
                             Promotion, SeasonalPlan, Category, Subcategory, Supplier,
                             SalesOrder, PurchaseOrder)
from routes.auth_routes import login_required, role_required, handle_errors
from sqlalchemy import func
import calendar

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ── /api/me ──────────────────────────────────────────────
@api_bp.route('/me')
@login_required
@handle_errors
def me():
    user = db.session.get(User, session['user_id'])
    if not user:
        return jsonify({}), 404
    mgr = Manager.query.filter_by(user_id=user.id).first()
    site = None
    if mgr and mgr.site_id:
        site = Site.query.filter_by(site_id=mgr.site_id).first()
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'site_id': mgr.site_id if mgr else None,
        'site_name': site.site_name if site else None,
    })


# ── /api/users ────────────────────────────────────────────
@api_bp.route('/users')
@login_required
@role_required('admin')
@handle_errors
def users_list():
    all_users = User.query.order_by(User.id.desc()).all()
    managers  = {m.user_id: m for m in Manager.query.all()}
    result = []
    for u in all_users:
        mgr = managers.get(u.id)
        site = None
        if mgr and mgr.site_id:
            site = Site.query.filter_by(site_id=mgr.site_id).first()
        d = u.to_dict()
        d['site_id']   = mgr.site_id if mgr else None
        d['site_name'] = site.site_name if site else None
        result.append(d)
    return jsonify({'users': result})


# ── /api/sites-list ───────────────────────────────────────
@api_bp.route('/sites-list')
@login_required
@handle_errors
def sites_list():
    sites = Site.query.order_by(Site.site_name).all()
    return jsonify({'sites': [{
        'site_id':     s.site_id,
        'site_name':   s.site_name,
        'site_format': s.site_format,
        'region':      s.region,
        'city':        s.city,
        'store_size':  s.store_size,
        'open_date':   str(s.open_date) if s.open_date else None,
        'status':      s.status,
    } for s in sites]})


# ── /api/products-list ────────────────────────────────────
@api_bp.route('/products-list')
@login_required
@handle_errors
def products_list():
    prods = Product.query.filter(Product.status != 'Inactive').order_by(Product.product_name).all()
    return jsonify({'products': [{
        'product_id':   p.product_id,
        'product_name': p.product_name,
        'category':     p.category,
        'unit_price':   p.unit_price,
        'unit_cost':    p.unit_cost,
    } for p in prods]})


# ── /api/dashboard/stats ─────────────────────────────────
@api_bp.route('/dashboard/stats')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def dashboard_stats():
    total_revenue  = db.session.query(func.sum(Sale.revenue)).scalar() or 0
    units_sold     = db.session.query(func.sum(Sale.units_sold)).scalar() or 0
    stockout_count = Inventory.query.filter_by(stockout_flag='Yes').count()
    active_sites   = Site.query.filter_by(status='Active').count()
    total_users    = User.query.count()
    total_products = Product.query.count()
    return jsonify({
        'total_revenue':  float(total_revenue),
        'units_sold':     int(units_sold),
        'stockout_count': stockout_count,
        'active_sites':   active_sites,
        'total_users':    total_users,
        'total_products': total_products,
    })


# ── /api/dashboard/revenue-trend ─────────────────────────
@api_bp.route('/dashboard/revenue-trend')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def revenue_trend():
    rows = (db.session.query(
                func.to_char(Sale.date, 'YYYY-MM').label('month'),
                func.sum(Sale.revenue).label('rev'))
            .group_by('month')
            .order_by('month')
            .limit(12).all())
    labels, values = [], []
    for r in rows:
        if r.month:
            try:
                y, m = r.month.split('-')
                labels.append(f"{calendar.month_abbr[int(m)]}-{y}")
            except Exception:
                labels.append(r.month)
        else:
            labels.append('—')
        values.append(float(r.rev or 0))
    return jsonify({'labels': labels, 'values': values})


# ── /api/dashboard/category-revenue ──────────────────────
@api_bp.route('/dashboard/category-revenue')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def category_revenue():
    rows = (db.session.query(
                Product.category,
                func.sum(Sale.revenue).label('rev'))
            .join(Sale, Sale.product_id == Product.product_id, isouter=True)
            .group_by(Product.category)
            .order_by(func.sum(Sale.revenue).desc())
            .limit(6).all())
    labels = [r.category or 'Unknown' for r in rows]
    values = [float(r.rev or 0) for r in rows]
    return jsonify({'labels': labels, 'values': values})


# ── /api/dashboard/recent-sales ──────────────────────────
@api_bp.route('/dashboard/recent-sales')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def recent_sales():
    rows = (db.session.query(Sale, Product, Site)
            .join(Product, Sale.product_id == Product.product_id, isouter=True)
            .join(Site,    Sale.site_id    == Site.site_id,       isouter=True)
            .order_by(Sale.date.desc()).limit(10).all())
    sales = [{
        'product': p.product_name if p else None,
        'site':    s.site_name    if s else None,
        'revenue': float(sale.revenue or 0),
        'date':    str(sale.date) if sale.date else None,
    } for sale, p, s in rows]
    return jsonify({'sales': sales})


# ── /api/dashboard/pending-shipments ─────────────────────
@api_bp.route('/dashboard/pending-shipments')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def pending_shipments():
    rows = (db.session.query(Logistics, Product, Site)
            .join(Product, Logistics.product_id == Product.product_id, isouter=True)
            .join(Site,    Logistics.site_id    == Site.site_id,       isouter=True)
            .filter(Logistics.delivery_status.in_(['Pending', 'In Transit', 'Delayed']))
            .order_by(Logistics.shipment_date.desc()).limit(8).all())
    shipments = [{
        'product': p.product_name  if p else None,
        'site':    s.site_name     if s else None,
        'status':  l.delivery_status,
    } for l, p, s in rows]
    return jsonify({'shipments': shipments})


# ── /admin/products/list (paginated JSON) ─────────────────
# (registered under admin prefix in app.py)


# ── /api/states ───────────────────────────────────────────
@api_bp.route('/states')
@login_required
@handle_errors
def states_list():
    from models.records import States
    states = States.query.order_by(States.state_name).all()
    return jsonify({'states': [{'state_id': s.state_id, 'state_name': s.state_name} for s in states]})


# ── /api/sites-by-state/<state_id> ───────────────────────
@api_bp.route('/sites-by-state/<int:state_id>')
@login_required
@handle_errors
def sites_by_state(state_id):
    sites = Site.query.filter_by(state_id=state_id, status='Active').order_by(Site.site_name).all()
    return jsonify({'sites': [{'site_id': s.site_id, 'site_name': s.site_name, 'city': s.city} for s in sites]})


# ── /api/dashboard/shipment-status-breakdown ─────────────
@api_bp.route('/dashboard/shipment-status-breakdown')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def shipment_status_breakdown():
    """Donut chart: count of each delivery_status across all logistics records."""
    rows = (db.session.query(Logistics.delivery_status, func.count(Logistics.id))
            .group_by(Logistics.delivery_status).all())
    labels = [r[0] or 'Unknown' for r in rows]
    values = [r[1] for r in rows]
    return jsonify({'labels': labels, 'values': values})


# ── /api/dashboard/transport-mode-breakdown ───────────────
@api_bp.route('/dashboard/transport-mode-breakdown')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def transport_mode_breakdown():
    """Bar chart: shipment quantity by transportation_type."""
    rows = (db.session.query(
                Logistics.transportation_type,
                func.count(Logistics.id).label('count'),
                func.sum(Logistics.quantity).label('qty'))
            .group_by(Logistics.transportation_type).all())
    labels = [r.transportation_type or 'Unknown' for r in rows]
    counts = [r.count for r in rows]
    quantities = [int(r.qty or 0) for r in rows]
    return jsonify({'labels': labels, 'counts': counts, 'quantities': quantities})


# ── /api/dashboard/top-sites-revenue ─────────────────────
@api_bp.route('/dashboard/top-sites-revenue')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def top_sites_revenue():
    """Horizontal bar: top 8 sites by total revenue."""
    rows = (db.session.query(Site.site_name, func.sum(Sale.revenue).label('rev'))
            .join(Sale, Sale.site_id == Site.site_id, isouter=True)
            .group_by(Site.site_name)
            .order_by(func.sum(Sale.revenue).desc())
            .limit(8).all())
    labels = [r.site_name or 'Unknown' for r in rows]
    values = [float(r.rev or 0) for r in rows]
    return jsonify({'labels': labels, 'values': values})


# ── /api/dashboard/inventory-status ──────────────────────
@api_bp.route('/dashboard/inventory-status')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def inventory_status():
    """Donut: stockout vs healthy vs low-stock inventory items."""
    stockout = Inventory.query.filter_by(stockout_flag='Yes').count()
    total    = Inventory.query.count()
    healthy  = total - stockout
    return jsonify({
        'labels': ['Healthy Stock', 'Stockout'],
        'values': [healthy, stockout],
    })


# ── /api/dashboard/monthly-shipments ─────────────────────
@api_bp.route('/dashboard/monthly-shipments')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def monthly_shipments():
    """Line chart: number of shipments per month (last 12 months)."""
    rows = (db.session.query(
                func.to_char(Logistics.shipment_date, 'YYYY-MM').label('month'),
                func.count(Logistics.id).label('cnt'))
            .group_by('month')
            .order_by('month')
            .limit(12).all())
    labels, values = [], []
    for r in rows:
        if r.month:
            try:
                y, m = r.month.split('-')
                labels.append(f"{calendar.month_abbr[int(m)]}-{y}")
            except Exception:
                labels.append(r.month)
        else:
            labels.append('—')
        values.append(r.cnt or 0)
    return jsonify({'labels': labels, 'values': values})


# ── /api/dashboard/sales-trend ───────────────────────────
@api_bp.route('/dashboard/sales-trend')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def sales_trend():
    """Line chart: monthly revenue and units sold from Sales table."""
    rows = (db.session.query(
                func.to_char(Sale.date, 'YYYY-MM').label('month'),
                func.sum(Sale.revenue).label('revenue'),
                func.sum(Sale.units_sold).label('units'))
            .group_by('month')
            .order_by('month')
            .limit(12).all())
    labels, revenues, units = [], [], []
    for r in rows:
        if r.month:
            try:
                y, m = r.month.split('-')
                labels.append(f"{calendar.month_abbr[int(m)]}-{y}")
            except Exception:
                labels.append(r.month)
        else:
            labels.append('—')
        revenues.append(float(r.revenue or 0))
        units.append(int(r.units or 0))
    return jsonify({'labels': labels, 'revenues': revenues, 'units': units})


# ── /api/dashboard/top-products-sold ────────────────────
@api_bp.route('/dashboard/top-products-sold')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def top_products_sold():
    """Bar chart: top 10 products by units sold."""
    rows = (db.session.query(Product.product_name, func.sum(Sale.units_sold).label('sold'))
            .join(Sale, Sale.product_id == Product.product_id, isouter=True)
            .group_by(Product.product_name)
            .order_by(func.sum(Sale.units_sold).desc())
            .limit(10).all())
    return jsonify({
        'labels': [r.product_name or 'Unknown' for r in rows],
        'values': [int(r.sold or 0) for r in rows],
    })


# ── /api/dashboard/inventory-by-site ────────────────────
@api_bp.route('/dashboard/inventory-by-site')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def inventory_by_site():
    """Bar chart: total ending inventory per site (top 10)."""
    rows = (db.session.query(Site.site_name, func.sum(Inventory.ending_inventory).label('qty'))
            .join(Inventory, Inventory.site_id == Site.site_id, isouter=True)
            .group_by(Site.site_name)
            .order_by(func.sum(Inventory.ending_inventory).desc())
            .limit(10).all())
    return jsonify({
        'labels': [r.site_name or 'Unknown' for r in rows],
        'values': [int(r.qty or 0) for r in rows],
    })


# ── /api/dashboard/sales-orders-status ──────────────────
@api_bp.route('/dashboard/sales-orders-status')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def sales_orders_status():
    """Donut: sales order status breakdown."""
    rows = (db.session.query(SalesOrder.status, func.count(SalesOrder.id))
            .group_by(SalesOrder.status).all())
    return jsonify({
        'labels': [r[0] or 'Unknown' for r in rows],
        'values': [r[1] for r in rows],
    })


# ── /api/dashboard/purchase-orders-status ───────────────
@api_bp.route('/dashboard/purchase-orders-status')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def purchase_orders_status():
    """Donut: purchase order status breakdown."""
    rows = (db.session.query(PurchaseOrder.status, func.count(PurchaseOrder.id))
            .group_by(PurchaseOrder.status).all())
    return jsonify({
        'labels': [r[0] or 'Unknown' for r in rows],
        'values': [r[1] for r in rows],
    })


# ── /api/dashboard/revenue-by-category ──────────────────
@api_bp.route('/dashboard/revenue-by-category')
@login_required
@role_required('admin','manager','analyst')
@handle_errors
def revenue_by_category():
    """Bar chart: total revenue per product category."""
    rows = (db.session.query(Product.category, func.sum(Sale.revenue).label('rev'))
            .join(Sale, Sale.product_id == Product.product_id, isouter=True)
            .group_by(Product.category)
            .order_by(func.sum(Sale.revenue).desc())
            .limit(8).all())
    return jsonify({
        'labels': [r.category or 'Unknown' for r in rows],
        'values': [float(r.rev or 0) for r in rows],
    })
