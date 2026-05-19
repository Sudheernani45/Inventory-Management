"""
admin_json_routes.py – JSON list endpoints for async/await JS frontend tables.
Registered under /admin prefix.
"""
from flask import Blueprint, request, jsonify, session
from models.db import db
from models.records import (Product, Site, Inventory, Logistics, Sale,
                             Promotion, SeasonalPlan, Category, Subcategory, Supplier,
                             SalesOrder, PurchaseOrder, Customer)
from routes.auth_routes import login_required, role_required, handle_errors
from sqlalchemy import func
import json

admin_json_bp = Blueprint('admin_json', __name__)


# ── Products list ─────────────────────────────────────────
@admin_json_bp.route('/products/list')
@login_required
@role_required('admin')
@handle_errors
def products_list():
    page     = request.args.get('page', 1, type=int)
    q        = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    site_id  = request.args.get('site_id', '').strip()
    per_page = request.args.get('per_page', 20, type=int)

    query = Product.query
    if q:
        query = query.filter(Product.product_name.ilike(f'%{q}%'))
    if category:
        query = query.filter_by(category=category)

    total = query.count()
    items = query.order_by(Product.product_id).offset((page - 1) * per_page).limit(per_page).all()

    # Build sales counts per product (optionally per site)
    sales_q = db.session.query(Sale.product_id, func.sum(Sale.units_sold).label('sold'))
    if site_id:
        sales_q = sales_q.filter(Sale.site_id == site_id)
    sales_map = {r.product_id: int(r.sold or 0) for r in sales_q.group_by(Sale.product_id).all()}

    # Build purchase counts per product from approved POs
    po_map = {}
    for r in db.session.query(PurchaseOrder).filter(PurchaseOrder.status == 'Approved').all():
        sid = (r.site or '').split(' - ')[0].strip()
        if not site_id or sid == site_id:
            po_map[r.product_id] = po_map.get(r.product_id, 0) + (r.quantity or 0)

    # Stock qty from inventory
    inv_q = Inventory.query
    if site_id:
        inv_q = inv_q.filter_by(site_id=site_id)
    inv_map = {r.product_id: (r.ending_inventory or 0) for r in inv_q.all()}

    return jsonify({
        'products': [{
            'product_id':   p.product_id,
            'product_name': p.product_name,
            'category':     p.category,
            'subcategory':  p.subcategory,
            'unit_cost':    float(p.unit_cost or 0),
            'unit_price':   float(p.unit_price or 0),
            'supplier':     p.supplier,
            'shelf_life':   p.shelf_life,
            'stock_qty':    inv_map.get(p.product_id),
            'times_sold':   sales_map.get(p.product_id, 0),
            'times_purchased': po_map.get(p.product_id, 0),
        } for p in items],
        'total':    total,
        'page':     page,
        'per_page': per_page,
    })


# ── Inventory list ────────────────────────────────────────
@admin_json_bp.route('/inventory/list')
@login_required
@role_required('admin')
@handle_errors
def inventory_list():
    page     = request.args.get('page', 1, type=int)
    stockout = request.args.get('stockout', '').strip()
    site_f   = request.args.get('site_id', '').strip()
    q        = request.args.get('q', '').strip()
    per_page = 20

    query = (db.session.query(Inventory, Product, Site)
             .join(Product, Inventory.product_id == Product.product_id, isouter=True)
             .join(Site,    Inventory.site_id    == Site.site_id,       isouter=True))
    if stockout == 'yes':
        query = query.filter(Inventory.stockout_flag == 'Yes')
    if site_f:
        query = query.filter(Inventory.site_id == site_f)
    if q:
        query = query.filter(Product.product_name.ilike(f'%{q}%'))

    total   = query.count()
    records = query.order_by(Inventory.id.desc()).offset((page - 1) * per_page).limit(per_page).all()

    # Build sales and purchase totals per product per site
    sales_totals = {}
    sales_rows = db.session.query(
        Sale.product_id, Sale.site_id,
        func.sum(Sale.units_sold).label('total_sold')
    ).group_by(Sale.product_id, Sale.site_id).all()
    for r in sales_rows:
        sales_totals[(r.product_id, r.site_id)] = int(r.total_sold or 0)

    po_totals = {}
    po_rows = db.session.query(
        PurchaseOrder.product_id, PurchaseOrder.site,
        func.sum(PurchaseOrder.quantity).label('total_purchased')
    ).filter(PurchaseOrder.status == 'Approved').group_by(PurchaseOrder.product_id, PurchaseOrder.site).all()
    for r in po_rows:
        # site column may be "SITE001 - Name"
        sid = (r.site or '').split(' - ')[0].strip()
        po_totals[(r.product_id, sid)] = int(r.total_purchased or 0)

    result = []
    for inv, p, s in records:
        pid = inv.product_id or ''
        sid = inv.site_id or ''
        total_sold      = sales_totals.get((pid, sid), 0)
        total_purchased = po_totals.get((pid, sid), 0)
        unit_cost  = float(p.unit_cost  or 0) if p else 0
        unit_price = float(p.unit_price or 0) if p else 0
        profit_margin = round(((unit_price - unit_cost) / unit_price * 100), 2) if unit_price > 0 else 0
        result.append({
            'product_id':       pid,
            'product_name':     p.product_name if p else None,
            'site_name':        s.site_name    if s else None,
            'site_id':          sid,
            'beginning_inventory': inv.beginning_inventory or 0,
            'ending_inventory':    inv.ending_inventory or 0,
            'stock_level':         inv.ending_inventory or 0,
            'total_sold':          total_sold,
            'total_purchased':     total_purchased,
            'stockout_flag':       inv.stockout_flag,
            'replenishment':       inv.replenishment or 0,
            'unit_cost':           unit_cost,
            'unit_price':          unit_price,
            'profit_margin':       profit_margin,
            'category':            p.category if p else None,
            'subcategory':         p.subcategory if p else None,
            'supplier':            p.supplier if p else None,
            'shelf_life':          p.shelf_life if p else None,
        })

    return jsonify({
        'records': result,
        'total': total, 'page': page, 'per_page': per_page,
    })


# ── Shipments global stats (for stat cards — counts across ALL records) ───
@admin_json_bp.route('/shipments/stats')
@login_required
@role_required('admin')
@handle_errors
def shipments_stats():
    """Returns total counts per delivery_status in a single aggregated SQL query."""
    rows = (db.session.query(Logistics.delivery_status, func.count(Logistics.id))
            .group_by(Logistics.delivery_status).all())
    counts = {status: cnt for status, cnt in rows}
    total = sum(counts.values())
    return jsonify({
        'total':       total,
        'in_transit':  counts.get('In Transit', 0),
        'delivered':   counts.get('Delivered', 0),
        'pending':     counts.get('Pending', 0),
        'delayed':     counts.get('Delayed', 0),
        'cancelled':   counts.get('Cancelled', 0),
    })


# ── Shipments list ────────────────────────────────────────
@admin_json_bp.route('/shipments/list')
@login_required
@role_required('admin')
@handle_errors
def shipments_list():
    page     = request.args.get('page', 1, type=int)
    status   = request.args.get('status', '').strip()
    q        = request.args.get('q', '').strip()
    ttype    = request.args.get('ttype', '').strip()   # FIX: server-side transport filter
    per_page = 20

    # FIX: single joined query — no N+1, no separate count round-trip
    query = (db.session.query(Logistics, Product, Site)
             .join(Product, Logistics.product_id == Product.product_id, isouter=True)
             .join(Site,    Logistics.site_id    == Site.site_id,       isouter=True))

    # All filters applied in SQL — never in Python
    if status:
        query = query.filter(Logistics.delivery_status == status)
    if ttype:
        query = query.filter(Logistics.transportation_type == ttype)  # FIX: was client-side
    if q:
        query = query.filter(
            db.or_(
                Product.product_name.ilike(f'%{q}%'),
                Logistics.shipment_id.ilike(f'%{q}%'),   # FIX: also search by shipment ID
                Site.site_name.ilike(f'%{q}%'),
            )
        )

    # FIX: use func.count on a subquery — single SQL round-trip for total
    total   = query.with_entities(func.count(Logistics.id)).scalar()
    records = (query
               .order_by(Logistics.shipment_date.desc())
               .offset((page - 1) * per_page)
               .limit(per_page)
               .all())

    return jsonify({
        'records': [{
            'shipment_id':         l.shipment_id,
            'product_name':        p.product_name        if p else None,
            'site_name':           s.site_name           if s else None,
            'quantity':            l.quantity,
            'shipment_date':       str(l.shipment_date)  if l.shipment_date else None,
            'delivery_date':       getattr(l, 'delivery_date', None) or '',
            'carrier':             l.transportation_type or 'Truck',
            'transportation_type': l.transportation_type or 'Truck',
            'delivery_status':     l.delivery_status,
            'site_id':             l.site_id,
            'product_id':          l.product_id,
        } for l, p, s in records],
        'total': total, 'page': page, 'per_page': per_page,
    })


# ── Sales list ────────────────────────────────────────────
@admin_json_bp.route('/sales/list')
@login_required
@role_required('admin')
@handle_errors
def sales_list():
    page     = request.args.get('page', 1, type=int)
    site_f   = request.args.get('site_id', '').strip()
    q        = request.args.get('q', '').strip()
    per_page = 20

    query = (db.session.query(Sale, Product, Site)
             .join(Product, Sale.product_id == Product.product_id, isouter=True)
             .join(Site,    Sale.site_id    == Site.site_id,       isouter=True))
    if site_f:
        query = query.filter(Sale.site_id == site_f)
    if q:
        query = query.filter(Product.product_name.ilike(f'%{q}%'))

    summary_q = db.session.query(
        func.sum(Sale.revenue).label('total_revenue'),
        func.sum(Sale.units_sold).label('total_units'),
        func.sum(Sale.returns).label('total_returns'),
        func.sum(Sale.discounts).label('total_discounts'),
    )
    if site_f:
        summary_q = summary_q.filter(Sale.site_id == site_f)
    summary = summary_q.first()

    total   = query.count()
    records = query.order_by(Sale.date.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        'records': [{
            'product_name': p.product_name if p else None,
            'site_name':    s.site_name    if s else None,
            'units_sold':   sale.units_sold,
            'revenue':      float(sale.revenue   or 0),
            'returns':      float(sale.returns   or 0),
            'discounts':    float(sale.discounts or 0),
            'date':         str(sale.date) if sale.date else None,
        } for sale, p, s in records],
        'summary': {
            'total_revenue':   float(summary.total_revenue   or 0),
            'total_units':     int(summary.total_units       or 0),
            'total_returns':   float(summary.total_returns   or 0),
            'total_discounts': float(summary.total_discounts or 0),
        },
        'total': total, 'page': page, 'per_page': per_page,
    })


# ── Promotions list ───────────────────────────────────────
@admin_json_bp.route('/promotions/list')
@login_required
@role_required('admin')
@handle_errors
def promotions_list():
    page     = request.args.get('page', 1, type=int)
    q        = request.args.get('q', '').strip()
    per_page = 20

    query = (db.session.query(Promotion, Product, Site)
               .join(Product, Promotion.product_id == Product.product_id, isouter=True)
               .join(Site,    Promotion.site_id    == Site.site_id,       isouter=True))
    if q:
        query = query.filter(Product.product_name.ilike(f'%{q}%'))

    total = query.count()
    records = query.order_by(Promotion.start_date.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        'records': [{
            'product_name':        p.product_name if p else None,
            'site_name':           s.site_name    if s else None,
            'discount_percentage': float(promo.discount_amount or 0),
            'promotion_type': promo.discount_type,
            'start_date':          str(promo.start_date) if promo.start_date else None,
            'end_date':            str(promo.end_date)   if promo.end_date   else None,
            'units_sold': None,
        } for promo, p, s in records],
        'total': total, 'page': page, 'per_page': per_page,
    })


# ── Seasonal plan list ────────────────────────────────────
@admin_json_bp.route('/seasonal-plan/list')
@login_required
@role_required('admin')
@handle_errors
def seasonal_plan_list():
    records = SeasonalPlan.query.order_by(SeasonalPlan.month).all()
    return jsonify({
        'records': [{
            'month':           r.month,
            'season': None,
            'holiday': None,
            'expected_demand': r.forecasted_sales,
            'promo_budget': float(r.actual_sales or 0),
            'top_category': r.product_category,
        } for r in records]
    })


# ── Monthly Inventory Metrics (sold / profit / replenishment) ────────────────
@admin_json_bp.route('/dashboard/monthly-inventory-metrics')
@login_required
@role_required('admin','analyst')
@handle_errors
def monthly_inventory_metrics_json():
    from models.records import Product as Prod, Inventory as Inv, PurchaseOrder as PO
    # PostgreSQL-compatible month grouping
    month_expr = func.to_char(Sale.date, 'YYYY-MM')
    rows = db.session.query(
        month_expr.label('month'),
        func.sum(Sale.units_sold).label('units_sold'),
        func.sum(Sale.revenue).label('revenue'),
    ).group_by(month_expr).order_by(month_expr).all()

    # Real profit calculation
    profit_rows = db.session.query(
        func.to_char(Sale.date, 'YYYY-MM').label('month'),
        func.sum((Sale.revenue - Sale.discounts) - Sale.units_sold * Product.unit_cost).label('profit')
    ).join(Product, Sale.product_id == Product.product_id, isouter=True).group_by(
        func.to_char(Sale.date, 'YYYY-MM')
    ).all()
    profit_map = {r.month: round(float(r.profit or 0), 2) for r in profit_rows}

    # Replenishment from POs per month
    po_rows = db.session.query(
        func.to_char(func.cast(PO.created_at, db.Date), 'YYYY-MM').label('month'),
        func.sum(PO.quantity).label('qty')
    ).filter(PO.status == 'Approved').group_by(
        func.to_char(func.cast(PO.created_at, db.Date), 'YYYY-MM')
    ).all()
    replen_map = {rr.month: int(rr.qty or 0) for rr in po_rows if rr.month}

    total_replen = int(db.session.query(func.sum(Inv.replenishment)).scalar() or 0)
    months = [r.month for r in rows if r.month][-12:]
    return jsonify({
        'labels':        months,
        'units_sold':    [int(next((r.units_sold or 0 for r in rows if r.month == m), 0)) for m in months],
        'profit':        [profit_map.get(m, 0) for m in months],
        'revenue':       [round(float(next((r.revenue or 0 for r in rows if r.month == m), 0)), 2) for m in months],
        'replenishment': [replen_map.get(m, 0) for m in months],
        'total_replenishment': total_replen,
        'total_profit':  round(sum(profit_map.get(m, 0) for m in months), 2),
        'total_units':   sum(int(next((r.units_sold or 0 for r in rows if r.month == m), 0)) for m in months),
    })


# ── Customer stats endpoint ───────────────────────────────
@admin_json_bp.route('/customers/stats')
@login_required
@role_required('admin','analyst')
@handle_errors
def customer_stats_json():
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


# ── Customer list endpoint ────────────────────────────────
@admin_json_bp.route('/customers/list')
@login_required
@role_required('admin')
@handle_errors
def customer_list_json():
    from models.records import Sale
    page     = request.args.get('page', 1, type=int)
    q        = request.args.get('q', '').strip()
    gender_f = request.args.get('gender', '').strip()
    income_f = request.args.get('income', '').strip()
    per_page = 20
    query = Customer.query
    if q:      query = query.filter(Customer.customer_id.ilike(f'%{q}%'))
    if gender_f: query = query.filter_by(gender=gender_f)
    if income_f: query = query.filter_by(income_bracket=income_f)
    total = query.count()
    items = query.order_by(Customer.id).offset((page-1)*per_page).limit(per_page).all()
    # Compute spend dynamically from Sales table
    cust_ids = [c.customer_id for c in items]
    spend_rows = db.session.query(
        Sale.customer_id,
        func.sum(Sale.revenue).label('total'),
        func.avg(Sale.revenue).label('avg'),
        func.count(Sale.id).label('freq')
    ).filter(Sale.customer_id.in_(cust_ids)).group_by(Sale.customer_id).all()
    spend_map = {r.customer_id: r for r in spend_rows}
    result = []
    for c in items:
        d = c.to_dict()
        sr = spend_map.get(c.customer_id)
        if sr:
            d['total_spend']   = round(float(sr.total or 0), 2)
            d['average_spend'] = round(float(sr.avg   or 0), 2)
            d['purchase_frequency'] = int(sr.freq or 0)
        result.append(d)
    return jsonify({'customers': result, 'total': total, 'page': page, 'per_page': per_page})
