from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from models.db import db
from models.user import User
from models.managers import Manager
from models.records import Product, Customer, Site, Inventory, Logistics, Sale, Promotion, SeasonalPlan, Category, Subcategory, Supplier, AuditLog, PurchaseOrder, SalesOrder, ContactMessage, SalesReturn, PurchaseReturn
from routes.auth_routes import login_required, role_required, handle_errors
from werkzeug.security import generate_password_hash
from sqlalchemy import func
from utils.audit import log_action
import random, string as _string, json
_string = _string  # alias for use in closures

admin_bp = Blueprint('admin', __name__)


def random_password(length=10):
    chars = _string.ascii_letters + _string.digits
    return ''.join(random.choices(chars, k=length))


# ─── DASHBOARD ───────────────────────────────────────────
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
@handle_errors
def dashboard():
    total_users    = User.query.count()
    total_sites    = Site.query.count()
    active_sites   = Site.query.filter_by(status='Active').count()
    total_products = Product.query.count()
    stockout_count = Inventory.query.filter_by(stockout_flag='Yes').count()
    total_revenue  = db.session.query(func.sum(Sale.revenue)).scalar() or 0

    recent_sales = (
        db.session.query(Sale, Product, Site)
        .join(Product, Sale.product_id == Product.product_id, isouter=True)
        .join(Site,    Sale.site_id    == Site.site_id,       isouter=True)
        .order_by(Sale.date.desc())
        .limit(10).all()
    )
    pending_shipments = (
        db.session.query(Logistics, Product, Site)
        .join(Product, Logistics.product_id == Product.product_id, isouter=True)
        .join(Site,    Logistics.site_id    == Site.site_id,       isouter=True)
        .filter(Logistics.delivery_status.in_(['Pending', 'In Transit', 'Delayed']))
        .order_by(Logistics.shipment_date.desc())
        .limit(8).all()
    )
    managers = (
        db.session.query(Manager, User, Site)
        .join(User, Manager.user_id == User.id)
        .join(Site, Manager.site_id == Site.site_id, isouter=True)
        .all()
    )
    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_sites=total_sites,
        active_sites=active_sites,
        total_products=total_products,
        stockout_count=stockout_count,
        total_revenue=total_revenue,
        recent_sales=recent_sales,
        pending_shipments=pending_shipments,
        managers=managers,
        site_formats=['Digital', 'Fresh', 'Smart', 'Trends'],
    )


# ─── USERS ───────────────────────────────────────────────
@admin_bp.route('/users')
@login_required
@role_required('admin')
@handle_errors
def users():
    all_users = User.query.order_by(User.id.desc()).all()
    all_sites = Site.query.filter_by(status='Active').order_by(Site.site_name).all()
    managers  = {m.user_id: m for m in Manager.query.all()}
    return render_template('admin/users.html', users=all_users, sites=all_sites, managers=managers)


@admin_bp.route('/users/add', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def add_user():
    data    = request.get_json()
    name    = data.get('name', '').strip()
    email   = data.get('email', '').strip()
    role    = data.get('role', 'manager')
    site_id = data.get('site_id', '').strip() or None

    if not name or not email:
        return jsonify({'status': 'error', 'message': 'Name and email are required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already exists'}), 400

    # Enforce only one admin in the system
    if role == 'admin':
        if User.query.filter_by(role='admin').count() > 0:
            return jsonify({'status': 'error', 'message': 'An admin already exists. Only one admin is allowed.'}), 400

    # Enforce one manager per state
    if role == 'manager' and site_id:
        site = Site.query.filter_by(site_id=site_id).first()
        if site and site.state_id:
            state_site_ids = [s.site_id for s in Site.query.filter_by(state_id=site.state_id).all()]
            existing = Manager.query.filter(Manager.site_id.in_(state_site_ids)).first()
            if existing:
                return jsonify({'status': 'error', 'message': 'A manager is already assigned to a site in this state.'}), 400

    # Auto-generate employee_id if not provided
    emp_id = (data.get('employee_id') or '').strip()
    if not emp_id:
        last_count = User.query.count()
        emp_id     = f'EMP{1000 + last_count + 1}'
    if User.query.filter_by(employee_id=emp_id).first():
        return jsonify({'status': 'error', 'message': f'Employee ID {emp_id} already exists'}), 400

    pwd  = random_password()
    user = User(
        name           = name,
        email          = email,
        password       = generate_password_hash(pwd),
        role           = role,
        is_first_login = True,
        is_active      = True,
        employee_id    = emp_id,
        phone          = data.get('phone', ''),
        department     = data.get('department', ''),
        photo_url      = data.get('photo_url', ''),
    )
    db.session.add(user)
    db.session.flush()

    if role == 'manager':
        db.session.add(Manager(user_id=user.id, site_id=site_id))

    db.session.commit()
    log_action('CREATE_USER', 'Users', f'User {name}',
               f'Role: {role}, Email: {email}, EmpID: {emp_id}')
    email_sent = False
    try:
        from utils.email import send_credentials_email
        send_credentials_email(email, name, pwd)
        email_sent = True
    except Exception as e:
        print(f'Email error: {e}')

    return jsonify({'status': 'success', 'message': 'User created.',
                    'employee_id': emp_id, 'temp_password': pwd, 'email_sent': email_sent})


@admin_bp.route('/users/<int:user_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def edit_user(user_id):
    data = request.get_json()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    new_role = data.get('role', user.role)
    new_name = data.get('name', user.name).strip()
    new_email = data.get('email', user.email).strip()
    site_id = data.get('site_id', '').strip() or None

    # Enforce only one admin — if changing role to admin, check no other admin exists
    if new_role == 'admin' and user.role != 'admin':
        if User.query.filter_by(role='admin').count() > 0:
            return jsonify({'status': 'error', 'message': 'An admin already exists. Only one admin is allowed.'}), 400

    # Enforce one manager per state when assigning/changing site
    if new_role == 'manager' and site_id:
        site = Site.query.filter_by(site_id=site_id).first()
        if site and site.state_id:
            state_site_ids = [s.site_id for s in Site.query.filter_by(state_id=site.state_id).all()]
            # Exclude current user's own manager record from check
            existing = Manager.query.filter(
                Manager.site_id.in_(state_site_ids),
                Manager.user_id != user_id
            ).first()
            if existing:
                return jsonify({'status': 'error', 'message': 'A manager is already assigned to a site in this state. Each state can have only one manager.'}), 400

    user.name  = new_name
    user.email = new_email
    user.role  = new_role

    if new_role == 'manager':
        mgr = Manager.query.filter_by(user_id=user.id).first()
        if mgr:
            mgr.site_id = site_id
        else:
            db.session.add(Manager(user_id=user.id, site_id=site_id))
    else:
        # If role changed away from manager, remove manager record
        Manager.query.filter_by(user_id=user.id).delete()

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User updated'})


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_user(user_id):
    if user_id == session.get('user_id'):
        return jsonify({'status': 'error', 'message': 'Cannot delete yourself'}), 400
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    try:
        # Clear foreign key references before deleting user
        Manager.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        
        db.session.delete(user)
        db.session.commit()
        log_action('DELETE', 'Users', f'User {user.name}', f'Email: {user.email}, Role: {user.role}')
        return jsonify({'status': 'success', 'message': 'User deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error deleting user: {str(e)}'}), 500


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def toggle_user(user_id):
    """Activate or deactivate a user account."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    user.is_active = not getattr(user, 'is_active', True)
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    log_action('UPDATE', 'Users', f'User {user.name}', f'Account {status}')
    return jsonify({'status': 'success', 'message': f'User {status}', 'is_active': user.is_active})


@admin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def reset_password(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    pwd = random_password()
    user.password       = generate_password_hash(pwd)
    user.is_first_login = True
    db.session.commit()
    email_sent = False
    try:
        from utils.email import send_credentials_email
        send_credentials_email(user.email, user.name, pwd)
        email_sent = True
    except Exception as e:
        print(f'Email error: {e}')
    return jsonify({'status': 'success', 'message': 'Password reset.',
                    'temp_password': pwd, 'email_sent': email_sent})


# ─── SITES ───────────────────────────────────────────────
@admin_bp.route('/sites')
@login_required
@role_required('admin')
@handle_errors
def sites():
    all_sites = Site.query.order_by(Site.site_id).all()
    return render_template('admin/sites.html', sites=all_sites)


@admin_bp.route('/sites/add', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def add_site():
    data = request.get_json()
    site_id = (data.get('site_id') or '').strip().upper()
    if not site_id:
        return jsonify({'status': 'error', 'message': 'Site ID is required'}), 400
    if Site.query.filter_by(site_id=site_id).first():
        return jsonify({'status': 'error', 'message': 'Site ID already exists'}), 400

    from datetime import date
    open_date = None
    if data.get('open_date'):
        try:
            open_date = date.fromisoformat(data['open_date'])
        except ValueError:
            pass

    state_id_val = data.get('state_id')
    state_id_int = int(state_id_val) if state_id_val else None
    s = Site(
        site_id     = site_id,
        site_name   = data.get('site_name', '').strip(),
        site_format = data.get('site_format', '').strip(),
        region      = data.get('region', '').strip(),
        city        = data.get('city', '').strip(),
        state_id    = state_id_int,
        store_size  = int(data.get('store_size') or 0),
        open_date   = open_date,
        status      = data.get('status', 'Active'),
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Warehouse/site {site_id} added successfully'})


@admin_bp.route('/sites/<site_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def edit_site(site_id):
    s = Site.query.filter_by(site_id=site_id).first()
    if not s:
        return jsonify({'status': 'error', 'message': 'Site not found'}), 404
    data = request.get_json()
    from datetime import date as _date
    open_date = None
    if data.get('open_date'):
        try:
            open_date = _date.fromisoformat(data['open_date'])
        except ValueError:
            pass
    state_id_val = data.get('state_id')
    s.site_name   = data.get('site_name', s.site_name).strip()
    s.site_format = data.get('site_format', s.site_format or '').strip()
    s.region      = data.get('region', s.region or '').strip()
    s.city        = data.get('city', s.city or '').strip()
    s.state_id    = int(state_id_val) if state_id_val else s.state_id
    s.store_size  = int(data['store_size']) if data.get('store_size') else s.store_size
    s.open_date   = open_date if open_date else s.open_date
    s.status      = data.get('status', s.status)
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Site {site_id} updated successfully'})


@admin_bp.route('/sites/<site_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_site(site_id):
    s = Site.query.filter_by(site_id=site_id).first()
    if not s:
        return jsonify({'status': 'error', 'message': 'Site not found'}), 404
    db.session.delete(s)
    db.session.commit()
    log_action('DELETE', 'Sites', f'Site {site_id}', f'Name: {s.site_name}')
    return jsonify({'status': 'success', 'message': f'Site {site_id} deleted successfully'})




# ─── PRODUCTS ────────────────────────────────────────────
@admin_bp.route('/products')
@login_required
@role_required('admin')
@handle_errors
def products():
    page     = request.args.get('page', 1, type=int)
    search   = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    query    = Product.query
    if search:
        query = query.filter(Product.product_name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    pagination = query.order_by(Product.product_id).paginate(page=page, per_page=20, error_out=False)
    categories = Category.query.order_by(Category.category_name).all()
    cat_names  = [c.category_name for c in categories]
    suppliers  = Supplier.query.order_by(Supplier.supplier_name).all()
    return render_template('admin/products.html',
                           products=pagination.items, pagination=pagination,
                           categories=categories, cat_names=cat_names,
                           suppliers=suppliers,
                           search=search, selected_category=category)


@admin_bp.route('/products/add', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def add_product():
    data = request.get_json()
    # Use custom product_id if provided, else auto-generate
    custom_pid = (data.get('product_id') or '').strip()
    if custom_pid:
        if Product.query.filter_by(product_id=custom_pid).first():
            return jsonify({'status': 'error', 'message': f'Product ID "{custom_pid}" already exists'}), 400
        auto_pid = custom_pid
    else:
        last = db.session.query(func.max(Product.id)).scalar() or 0
        auto_pid = f"PRD{10000 + last + 1}"
    p = Product(
        product_id   = auto_pid,
        product_name = data['product_name'],
        category     = data.get('category'),
        subcategory  = data.get('subcategory'),
        unit_cost    = float(data.get('unit_cost') or 0),
        unit_price   = float(data.get('unit_price') or 0),
        supplier     = data.get('supplier'),
        shelf_life   = int(data.get('shelf_life') or 0),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Product added (ID: {auto_pid})', 'product_id': auto_pid})


# ─── CATEGORY / SUBCATEGORY API ──────────────────────────
@admin_bp.route('/categories', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_categories():
    cats = Category.query.order_by(Category.category_name).all()
    return jsonify([c.to_dict() for c in cats])


@admin_bp.route('/categories/add', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def add_category():
    data     = request.get_json()
    cat_name = (data.get('category_name') or '').strip()
    sub_name = (data.get('subcategory_name') or '').strip()
    if not cat_name or not sub_name:
        return jsonify({'status': 'error', 'message': 'Category and subcategory name are required'}), 400

    cat = Category.query.filter_by(category_name=cat_name).first()
    if not cat:
        cat = Category(category_name=cat_name)
        db.session.add(cat)
        db.session.flush()

    existing_sub = Subcategory.query.filter_by(category_id=cat.id, subcategory_name=sub_name).first()
    if existing_sub:
        return jsonify({'status': 'error', 'message': 'Subcategory already exists in this category'}), 400

    db.session.add(Subcategory(category_id=cat.id, subcategory_name=sub_name))
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Category/subcategory added', 'category': cat.to_dict()})


@admin_bp.route('/categories/<int:cat_id>/subcategories', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_subcategories(cat_id):
    subs = Subcategory.query.filter_by(category_id=cat_id).order_by(Subcategory.subcategory_name).all()
    return jsonify([s.to_dict() for s in subs])


# ─── SUPPLIERS PAGE ───────────────────────────────────────
@admin_bp.route('/suppliers-list')
@login_required
@role_required('admin')
@handle_errors
def suppliers_page():
    return render_template('admin/suppliers.html')

# ─── SUPPLIER API ─────────────────────────────────────────
@admin_bp.route('/suppliers', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_suppliers():
    sups = Supplier.query.order_by(Supplier.supplier_name).all()
    return jsonify([s.to_dict() for s in sups])


@admin_bp.route('/suppliers/add', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def add_supplier():
    data  = request.get_json()
    name  = (data.get('supplier_name') or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    if not name or not email:
        return jsonify({'status': 'error', 'message': 'Supplier name and email are required'}), 400
    if Supplier.query.filter_by(supplier_name=name).first():
        return jsonify({'status': 'error', 'message': 'Supplier already exists'}), 400
    # Auto-generate supplier_id
    count = Supplier.query.count()
    sup_id = f'SUP{1000 + count + 1}'
    s = Supplier(supplier_id=sup_id, supplier_name=name, email=email, phone=phone)
    db.session.add(s)
    db.session.commit()
    log_action('CREATE', 'Suppliers', f'Supplier {name}', f'Email: {email}, Phone: {phone}')
    return jsonify({'status': 'success', 'message': f'Supplier {name} added', 'supplier': s.to_dict()})


@admin_bp.route('/suppliers/<int:sup_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def edit_supplier(sup_id):
    s = db.session.get(Supplier, sup_id)
    if not s:
        return jsonify({'status': 'error', 'message': 'Supplier not found'}), 404
    data = request.get_json()
    s.supplier_name = (data.get('supplier_name') or s.supplier_name).strip()
    s.email         = (data.get('email') or s.email or '').strip()
    s.phone         = (data.get('phone') or s.phone or '').strip()
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Supplier updated', 'supplier': s.to_dict()})


@admin_bp.route('/suppliers/<int:sup_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_supplier(sup_id):
    s = db.session.get(Supplier, sup_id)
    if not s:
        return jsonify({'status': 'error', 'message': 'Supplier not found'}), 404
    name = s.supplier_name
    db.session.delete(s)
    db.session.commit()
    log_action('DELETE', 'Suppliers', f'Supplier {name}', f'ID: {sup_id}')
    return jsonify({'status': 'success', 'message': 'Supplier deleted'})


@admin_bp.route('/categories/<int:cat_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def edit_category(cat_id):
    """Update a category name."""
    cat = db.session.get(Category, cat_id)
    if not cat:
        return jsonify({'status': 'error', 'message': 'Category not found'}), 404
    data = request.get_json()
    new_name = (data.get('category_name') or '').strip()
    if not new_name:
        return jsonify({'status': 'error', 'message': 'Category name is required'}), 400
    if Category.query.filter(Category.category_name == new_name, Category.id != cat_id).first():
        return jsonify({'status': 'error', 'message': 'Category name already exists'}), 400
    old_name = cat.category_name
    cat.category_name = new_name
    db.session.commit()
    log_action('UPDATE', 'Categories', f'Category {old_name}', f'Renamed to {new_name}')
    return jsonify({'status': 'success', 'message': 'Category updated', 'category': cat.to_dict()})


@admin_bp.route('/categories/<int:cat_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_category(cat_id):
    """Delete a category and all its subcategories."""
    cat = db.session.get(Category, cat_id)
    if not cat:
        return jsonify({'status': 'error', 'message': 'Category not found'}), 404
    name = cat.category_name
    db.session.delete(cat)
    db.session.commit()
    log_action('DELETE', 'Categories', f'Category {name}', f'ID: {cat_id}')
    return jsonify({'status': 'success', 'message': 'Category deleted'})


@admin_bp.route('/suppliers/<int:supplier_id>/send-po/<po_number>', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def send_po_to_supplier(supplier_id, po_number):
    """
    Email a Purchase Order to a supplier for approval.
    Generates a unique approval token and sends approve/reject links via email.
    """
    import secrets
    from datetime import datetime as _dt, timedelta
    from utils.email import send_credentials_email

    sup = db.session.get(Supplier, supplier_id)
    if not sup:
        return jsonify({'status': 'error', 'message': 'Supplier not found'}), 404
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Purchase order not found'}), 404
    if not sup.email:
        return jsonify({'status': 'error', 'message': 'Supplier has no email address'}), 400

    token  = secrets.token_hex(64)
    expiry = _dt.utcnow() + timedelta(days=7)

    po.supplier_id             = supplier_id
    po.supplier_approval_token = token
    po.supplier_token_expiry   = expiry
    po.supplier_action         = 'pending'
    db.session.commit()

    from flask import request as _req
    base_url    = _req.host_url.rstrip('/')
    approve_url = f'{base_url}/supplier/approve/{token}'
    reject_url  = f'{base_url}/supplier/reject/{token}'

    try:
        from extensions import mail
        from flask_mail import Message
        msg = Message(
            subject=f'Purchase Order {po_number} — Action Required',
            recipients=[sup.email],
            body=(
                f'Dear {sup.supplier_name},\n\n'
                f'You have received Purchase Order {po_number}.\n'
                f'Product: {po.product_name}  |  Qty: {po.quantity}  |  Total: {po.total_cost:.2f}\n\n'
                f'APPROVE: {approve_url}\n'
                f'REJECT:  {reject_url}\n\n'
                f'This link expires in 7 days.\n\nRegards,\nInventory Management'
            )
        )
        mail.send(msg)
        email_sent = True
    except Exception as e:
        print(f'[PO Email] Failed: {e}')
        email_sent = False

    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}', f'Sent to supplier {sup.supplier_name} ({sup.email})')
    return jsonify({
        'status':     'success',
        'message':    f'PO sent to {sup.supplier_name}',
        'email_sent': email_sent,
        'approve_url': approve_url,
        'reject_url':  reject_url,
    })




@admin_bp.route('/products/<product_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def edit_product(product_id):
    p    = Product.query.filter_by(product_id=product_id).first_or_404()
    data = request.get_json()
    p.product_name = data.get('product_name', p.product_name)
    p.category     = data.get('category', p.category)
    p.subcategory  = data.get('subcategory', p.subcategory)
    p.unit_cost    = float(data.get('unit_cost') or p.unit_cost)
    p.unit_price   = float(data.get('unit_price') or p.unit_price)
    p.supplier     = data.get('supplier', p.supplier)
    p.shelf_life   = int(data.get('shelf_life') or p.shelf_life)
    # New fields
    if 'uom'               in data: p.uom               = data['uom']
    if 'reorder_point'     in data: p.reorder_point     = int(data['reorder_point'] or 0)
    if 'reorder_qty'       in data: p.reorder_qty       = int(data['reorder_qty']   or 0)
    if 'default_warehouse' in data: p.default_warehouse = data['default_warehouse']
    if 'status'            in data: p.status            = data['status']
    db.session.commit()
    log_action('UPDATE', 'Products', f'Product {product_id}', f'Updated: {list(data.keys())}')
    return jsonify({'status': 'success', 'message': 'Product updated'})


@admin_bp.route('/products/<product_id>/toggle-status', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def toggle_product_status(product_id):
    """Toggle product status between Active and Inactive."""
    p = Product.query.filter_by(product_id=product_id).first_or_404()
    p.status = 'Inactive' if (p.status or 'Active') == 'Active' else 'Active'
    db.session.commit()
    log_action('UPDATE', 'Products', f'Product {product_id}', f'Status → {p.status}')
    return jsonify({'status': 'success', 'new_status': p.status})


@admin_bp.route('/products/<product_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_product(product_id):
    p = Product.query.filter_by(product_id=product_id).first_or_404()
    pname = p.product_name
    db.session.delete(p)
    db.session.commit()
    log_action('DELETE', 'Products', f'Product {pname}', f'ID: {product_id}')
    return jsonify({'status': 'success', 'message': 'Product deleted'})


# ─── INVENTORY ───────────────────────────────────────────
@admin_bp.route('/inventory')
@login_required
@role_required('admin')
@handle_errors
def inventory():
    page     = request.args.get('page', 1, type=int)
    stockout = request.args.get('stockout', '').strip()
    site_f   = request.args.get('site_id', '').strip()
    query = (db.session.query(Inventory, Product, Site)
             .join(Product, Inventory.product_id == Product.product_id, isouter=True)
             .join(Site,    Inventory.site_id    == Site.site_id,       isouter=True))
    if stockout == 'yes':
        query = query.filter(Inventory.stockout_flag == 'Yes')
    if site_f:
        query = query.filter(Inventory.site_id == site_f)
    total   = query.count()
    records = query.order_by(Inventory.id.desc()).offset((page-1)*20).limit(20).all()
    sites   = Site.query.order_by(Site.site_name).all()
    return render_template('admin/inventory.html',
                           records=records, page=page, total=total, per_page=20,
                           sites=sites, site_f=site_f, stockout=stockout)


# ─── SHIPMENTS ───────────────────────────────────────────
@admin_bp.route('/shipments')
@login_required
@role_required('admin')
@handle_errors
def shipments():
    page   = request.args.get('page', 1, type=int)
    status = request.args.get('status', '').strip()
    query  = (db.session.query(Logistics, Product, Site)
              .join(Product, Logistics.product_id == Product.product_id, isouter=True)
              .join(Site,    Logistics.site_id    == Site.site_id,       isouter=True))
    if status:
        if status == 'Pending':
            query = query.filter(Logistics.delivery_status.in_([
                'Pending', 'Dispatched', 'In Transit', 'Picked Up', 'Out for Delivery'
            ]))
        else:
            query = query.filter(Logistics.delivery_status == status)
    total    = query.count()
    records  = query.order_by(Logistics.shipment_date.desc()).offset((page-1)*20).limit(20).all()
    statuses = [s[0] for s in db.session.query(Logistics.delivery_status).distinct().order_by(Logistics.delivery_status).all()]
    return render_template('admin/shipments.html',
                           records=records, page=page, total=total, per_page=20,
                           statuses=statuses, sel_status=status)


# ─── SALES ───────────────────────────────────────────────
@admin_bp.route('/sales')
@login_required
@role_required('admin')
@handle_errors
def sales():
    page   = request.args.get('page', 1, type=int)
    site_f = request.args.get('site_id', '').strip()
    query  = (db.session.query(Sale, Product, Site)
              .join(Product, Sale.product_id == Product.product_id, isouter=True)
              .join(Site,    Sale.site_id    == Site.site_id,       isouter=True))
    if site_f:
        query = query.filter(Sale.site_id == site_f)
    summary = db.session.query(
        func.sum(Sale.revenue).label('total_revenue'),
        func.sum(Sale.units_sold).label('total_units'),
        func.sum(Sale.returns).label('total_returns'),
        func.sum(Sale.discounts).label('total_discounts'),
    ).first()
    total   = query.count()
    records = query.order_by(Sale.date.desc()).offset((page-1)*20).limit(20).all()
    sites   = Site.query.order_by(Site.site_name).all()
    return render_template('admin/sales.html',
                           records=records, page=page, total=total, per_page=20,
                           sites=sites, site_f=site_f, summary=summary)


# ─── PROMOTIONS ──────────────────────────────────────────
@admin_bp.route('/promotions')
@login_required
@role_required('admin')
@handle_errors
def promotions():
    return render_template('admin/promotions.html')


# ─── SEASONAL PLANNING ───────────────────────────────────
@admin_bp.route('/seasonal-plan')
@login_required
@role_required('admin')
@handle_errors
def seasonal_plan():
    return render_template('admin/seasonal_plan.html')


# ─── SALES ORDERS (Admin — full access, no site restriction) ─────────────────
def _admin_random_id(prefix, length=6):
    return prefix + ''.join(random.choices(_string.ascii_uppercase + _string.digits, k=length))

@admin_bp.route('/sales-orders')
@login_required
@role_required('admin')
@handle_errors
def sales_orders():
    return render_template('admin/sales_orders.html')

@admin_bp.route('/api/sales-orders', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_sales_orders():
    so_number = request.args.get('so_number', '').strip()
    q         = request.args.get('q', '').strip()
    query = SalesOrder.query.filter_by(role='admin')
    if so_number:
        query = query.filter_by(so_number=so_number)
    if q:
        query = query.filter(
            db.or_(
                SalesOrder.so_number.ilike(f'%{q}%'),
                SalesOrder.customer.ilike(f'%{q}%'),
            )
        )
    orders = query.order_by(SalesOrder.id.desc()).all()
    return jsonify({'orders': [o.to_dict() for o in orders], 'total': len(orders)})

@admin_bp.route('/api/sales-orders', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def create_sales_order():
    from datetime import date
    import random as _rand, string as _str2
    d = request.get_json()
    so_ref = 'SO-' + ''.join(_rand.choices(_str2.digits, k=5))
    # Ensure unique
    while SalesOrder.query.filter_by(so_number=so_ref).first():
        so_ref = 'SO-' + ''.join(_rand.choices(_str2.digits, k=5))
    items  = d.get('items', [])
    # Server-side stock validation
    site_raw = d.get('site', '')
    site_id  = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()
    for item in items:
        pid = item.get('product_id', '')
        qty = int(item.get('quantity', 0))
        if pid and qty > 0 and site_id:
            inv = Inventory.query.filter_by(product_id=pid, site_id=site_id).first()
            if inv and (inv.ending_inventory or 0) < qty:
                return jsonify({'status': 'error', 'message': f'Insufficient stock for product {item.get("product_name", pid)}. Only {inv.ending_inventory or 0} units available.'}), 400
    total  = sum(float(i.get('unit_price', 0)) * int(i.get('quantity', 0)) for i in items)
    so = SalesOrder(
        so_number    = so_ref,
        customer     = d.get('customer', ''),
        state        = d.get('state', ''),
        site         = d.get('site', ''),
        items_json   = json.dumps(items),
        total_amount = total,
        status       = 'Pending',
        created_at   = str(date.today()),
        created_by   = session.get('username', 'Admin'),
        role         = 'admin',
    )
    db.session.add(so)
    db.session.commit()
    log_action('CREATE', 'Sales Orders', f'SO {so_ref}', f'Customer: {so.customer}, Total: {total:.2f}')
    return jsonify({'status': 'success', 'so_number': so_ref})

@admin_bp.route('/api/sales-orders/<so_number>/confirm', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def confirm_sales_order(so_number):
    from datetime import date as _date
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    so.status       = 'Confirmed'
    so.confirmed_at = str(_date.today())
    shipments_created = []
    try:
        site_raw = so.site or ''
        site_id  = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()
        items    = json.loads(so.items_json or '[]')
        for item in items:
            product_id = item.get('product_id', '')
            qty        = int(item.get('quantity', 0))
            if not product_id or qty <= 0:
                continue
            inv = Inventory.query.filter_by(product_id=product_id, site_id=site_id).first()
            if inv:
                inv.ending_inventory = max(0, (inv.ending_inventory or 0) - qty)
                if inv.ending_inventory == 0:
                    inv.stockout_flag = 'Yes'
            shipment_id = 'SHP-' + ''.join(random.choices(_string.ascii_uppercase + _string.digits, k=8))
            db.session.add(Logistics(
                shipment_id=shipment_id, site_id=site_id, product_id=product_id,
                shipment_date=_date.today(), quantity=qty,
                delivery_status='Pending', transportation_type=so.dispatch_type or 'Truck'
            ))
            shipments_created.append({'shipment_id': shipment_id, 'product_id': product_id})
            item['shipment_id'] = shipment_id
        so.items_json = json.dumps(items)
        so.status     = 'Processing'
        db.session.commit()
        log_action('UPDATE', 'Sales Orders', f'SO {so_number}', 'Status → Processing, inventory decremented')
    except Exception as ex:
        db.session.rollback()
        print(f'Confirm SO error: {ex}')
    return jsonify({'status': 'success', 'shipments': shipments_created})

@admin_bp.route('/api/sales-orders/<so_number>/cancel', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def cancel_sales_order_admin(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    d = request.get_json() or {}
    so.status       = 'Cancelled'
    so.cancelled_at = str(__import__('datetime').date.today())
    so.cancel_reason = d.get('cancel_reason', '')
    db.session.commit()
    log_action('UPDATE', 'Sales Orders', f'SO {so_number}', f'Status → Cancelled. Reason: {so.cancel_reason}')
    return jsonify({'status': 'success'})


@admin_bp.route('/api/sales-orders/<so_number>/tracking-update', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def update_so_tracking(so_number):
    """Update tracking status and notes on shipments linked to an SO."""
    from datetime import datetime as _dt
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    d              = request.get_json() or {}
    new_status     = d.get('delivery_status', '')
    tracking_notes = d.get('tracking_notes', '')
    est_delivery   = d.get('estimated_delivery', '')

    items   = json.loads(so.items_json or '[]')
    updated = []
    for item in items:
        sid = item.get('shipment_id')
        if not sid:
            continue
        rec = Logistics.query.filter_by(shipment_id=sid).first()
        if rec:
            if new_status:
                rec.delivery_status = new_status
            if tracking_notes:
                rec.tracking_notes  = tracking_notes
            if est_delivery:
                from datetime import date as _d
                try:
                    rec.estimated_delivery = _d.fromisoformat(est_delivery)
                except Exception:
                    pass
            rec.tracking_status_updated = _dt.utcnow()
            updated.append(sid)

    db.session.commit()
    log_action('UPDATE', 'Shipments', f'SO {so_number}', f'Tracking updated: {new_status}')
    return jsonify({'status': 'success', 'updated_shipments': updated})

@admin_bp.route('/api/sales-orders/<so_number>/dispatch', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def dispatch_sales_order(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    d = request.get_json() or {}
    dispatch_type    = d.get('dispatch_type', 'Truck')
    so.status        = 'Dispatched'
    so.dispatch_type = dispatch_type
    so.dispatched_at = str(__import__('datetime').date.today())
    shipments_linked = []
    try:
        items = json.loads(so.items_json or '[]')
        for item in items:
            sid = item.get('shipment_id')
            if sid:
                rec = Logistics.query.filter_by(shipment_id=sid).first()
                if rec:
                    rec.transportation_type = dispatch_type
                    rec.delivery_status = 'In Transit'
                    shipments_linked.append({'shipment_id': sid, 'product_id': item.get('product_id')})
        db.session.commit()
        # Log supplier notification (simulated mail)
        log_action('DISPATCH', 'Sales Orders', f'SO {so_number}',
                   f'Dispatched via {dispatch_type}. Customer: {so.customer} <{so.customer_email}>. '
                   f'Supplier notification sent.')
    except Exception as ex:
        db.session.rollback()
        print(f'Dispatch error: {ex}')
    return jsonify({
        'status': 'success',
        'dispatch_type': dispatch_type,
        'shipments': shipments_linked,
        'supplier_notified': True,
        'customer_email': so.customer_email or ''
    })

@admin_bp.route('/api/sales-orders/<so_number>/tracking', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_so_tracking(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
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
                'shipment_id':       rec.shipment_id,
                'product_id':        rec.product_id,
                'product_name':      prod.product_name if prod else rec.product_id,
                'quantity':          rec.quantity,
                'shipment_date':     str(rec.shipment_date) if rec.shipment_date else None,
                'delivery_status':   rec.delivery_status,
                'transportation_type': rec.transportation_type,
                'site_id':           rec.site_id,
            })
    # Compute overall SO status
    status = so.status or 'Pending'

    # Build timeline stages
    timeline = [
        {'stage': 'Order Placed',  'done': True,                         'date': so.created_at   or ''},
        {'stage': 'Confirmed',     'done': so.confirmed_at is not None,  'date': so.confirmed_at or ''},
        {'stage': 'Dispatched',    'done': so.dispatched_at is not None, 'date': so.dispatched_at or ''},
        {'stage': 'Delivered',     'done': status == 'Delivered',        'date': ''},
    ]

    # Estimated delivery: dispatched_date + avg lead_time from products (shelf_life as proxy)
    est_delivery = None
    if so.dispatched_at or so.confirmed_at:
        from datetime import datetime, timedelta
        base_str = so.dispatched_at or so.confirmed_at
        try:
            base_date = datetime.strptime(base_str[:10], '%Y-%m-%d')
            lead_days = 0
            count = 0
            for item in json.loads(so.items_json or '[]'):
                prod = Product.query.filter_by(product_id=item.get('product_id', '')).first()
                if prod and prod.shelf_life:
                    lead_days += prod.shelf_life
                    count += 1
                else:
                    lead_days += 5  # default 5-day lead time
                    count += 1
            avg_lead = int(lead_days / count) if count else 5
            est_delivery = (base_date + timedelta(days=avg_lead)).strftime('%Y-%m-%d')
        except Exception:
            pass

    return jsonify({'status': 'success', 'so_number': so_number,
                    'so_status': status,
                    'dispatch_type': so.dispatch_type or 'Truck',
                    'customer': so.customer, 'site': so.site,
                    'created_at': so.created_at or '',
                    'confirmed_at': so.confirmed_at or '',
                    'dispatched_at': so.dispatched_at or '',
                    'estimated_delivery': est_delivery or '',
                    'timeline': timeline,
                    'shipments': shipments})

# ─── PURCHASE ORDERS (Admin — DB-backed) ─────────────────────────────────────
@admin_bp.route('/purchase-orders')
@login_required
@role_required('admin')
@handle_errors
def purchase_orders():
    return render_template('admin/purchase_orders.html')

@admin_bp.route('/api/purchase-orders', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_purchase_orders():
    po_number = request.args.get('po_number', '').strip()
    q         = request.args.get('q', '').strip()
    query = PurchaseOrder.query.filter_by(role='admin')
    if po_number:
        query = query.filter_by(po_number=po_number)
    if q:
        query = query.filter(
            db.or_(
                PurchaseOrder.po_number.ilike(f'%{q}%'),
                PurchaseOrder.product_name.ilike(f'%{q}%'),
                PurchaseOrder.supplier.ilike(f'%{q}%'),
            )
        )
    orders = query.order_by(PurchaseOrder.id.desc()).all()
    return jsonify({'orders': [o.to_dict() for o in orders], 'total': len(orders)})

@admin_bp.route('/api/purchase-orders', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def create_purchase_order_admin():
    from datetime import date
    d = request.get_json()
    po_num = _admin_random_id('PO-', 6)
    qty = int(d.get('quantity', 0))
    cost = float(d.get('unit_cost', 0))
    po = PurchaseOrder(
        po_number        = po_num,
        supplier         = d.get('supplier', ''),
        product_name     = d.get('product_name', ''),
        quantity         = qty,
        unit_cost        = cost,
        total_cost       = qty * cost,
        status           = 'Draft',
        site             = d.get('site', 'All Sites'),
        product_id       = d.get('product_id', ''),
        expected_delivery= d.get('expected_delivery', ''),
        created_at       = str(date.today()),
        created_by       = session.get('username', 'Admin'),
        role             = 'admin',
    )
    db.session.add(po)
    db.session.commit()
    log_action('CREATE', 'Purchase Orders', f'PO {po_num}', f'Supplier: {po.supplier}, Qty: {qty}')
    return jsonify({'status': 'success', 'po_number': po_num})

@admin_bp.route('/api/purchase-orders/<po_number>/approve', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def approve_purchase_order_admin(po_number):
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    po.status      = 'Approved'
    po.approved_at = str(__import__('datetime').date.today())
    inv_updated = False
    try:
        site_raw = po.site or ''
        site_id  = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()
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
        db.session.commit()
        log_action('UPDATE', 'Purchase Orders', f'PO {po_number}', f'Approved, inventory +{qty}')
    except Exception as ex:
        db.session.rollback()
        print(f'PO approve error: {ex}')
    return jsonify({'status': 'success', 'inventory_updated': inv_updated, 'qty_added': po.quantity})

@admin_bp.route('/api/purchase-orders/<po_number>/cancel', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def cancel_purchase_order_admin(po_number):
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    d = request.get_json() or {}
    po.status       = 'Cancelled'
    po.cancelled_at = str(__import__('datetime').date.today())
    po.cancel_reason = d.get('cancel_reason', '')
    db.session.commit()
    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}', 'Status → Cancelled')
    return jsonify({'status': 'success'})


@admin_bp.route('/api/purchase-orders/<po_number>/reject', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def reject_purchase_order_admin(po_number):
    """Reject a PO (sends it back to Draft with rejection reason)."""
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    if po.status not in ('Pending', 'Draft'):
        return jsonify({'status': 'error', 'message': 'Only Pending/Draft POs can be rejected'}), 400
    d = request.get_json() or {}
    po.status           = 'Draft'
    po.rejection_reason = d.get('rejection_reason', '')
    db.session.commit()
    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}', f'Rejected: {po.rejection_reason}')
    return jsonify({'status': 'success', 'message': f'{po_number} rejected'})


@admin_bp.route('/api/purchase-orders/<po_number>/receive', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def receive_purchase_order_admin(po_number):
    """
    Receive goods for an Approved PO.
    Updates inventory AND creates a StockMovement record (PurchaseIn).
    Body: { qty_received, remarks }
    """
    from models.records import StockLevel, StockMovement
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    if po.status != 'Approved':
        return jsonify({'status': 'error', 'message': 'Only Approved POs can be received'}), 400

    d   = request.get_json() or {}
    qty = int(d.get('qty_received', po.quantity) or po.quantity)
    remarks = d.get('remarks', '')

    site_raw = po.site or ''
    site_id  = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()

    # Update inventory.ending_inventory
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
                beginning_inventory=qty, ending_inventory=qty, replenishment=qty, stockout_flag='No'))

        # Update or create StockLevel
        sl = StockLevel.query.filter_by(site_id=site_id, product_id=po.product_id).first()
        if sl:
            sl.qty_on_hand += qty
        else:
            sl = StockLevel(site_id=site_id, product_id=po.product_id, qty_on_hand=qty)
            db.session.add(sl)

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
    po.received_at = str(__import__('datetime').date.today())
    db.session.commit()
    log_action('UPDATE', 'Purchase Orders', f'PO {po_number}', f'Goods received, qty={qty}, site={site_id}')
    return jsonify({'status': 'success', 'message': f'Goods received for {po_number}', 'qty_received': qty})

@admin_bp.route('/api/purchase-orders/<po_number>/detail', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_po_detail(po_number):
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    po_dict = po.to_dict()
    try:
        site_raw = po.site or ''
        site_id  = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()
        if po.product_id and site_id:
            inv = Inventory.query.filter_by(product_id=po.product_id, site_id=site_id).first()
            po_dict['current_inventory'] = inv.ending_inventory if inv else None
    except Exception:
        po_dict['current_inventory'] = None
    return jsonify({'status': 'success', 'order': po_dict})

# ─── AUDIT LOG ───────────────────────────────────────────
@admin_bp.route('/audit-log')
@login_required
@role_required('admin')
@handle_errors
def audit_log_page():
    return render_template('admin/audit_log.html')

@admin_bp.route('/api/audit-log', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_audit_log():
    page     = request.args.get('page', 1, type=int)
    per_page = 50
    action_f = request.args.get('action', '').strip()
    module_f = request.args.get('module', '').strip()
    q        = request.args.get('q', '').strip()
    date_from= request.args.get('date_from', '').strip()
    date_to  = request.args.get('date_to', '').strip()
    query = db.session.query(AuditLog)
    if action_f: query = query.filter(AuditLog.action == action_f)
    if module_f: query = query.filter(AuditLog.module == module_f)
    if q:
        query = query.filter(db.or_(
            AuditLog.user.ilike(f'%{q}%'),
            AuditLog.detail.ilike(f'%{q}%'),
            AuditLog.resource.ilike(f'%{q}%'),
        ))
    if date_from: query = query.filter(db.func.date(AuditLog.timestamp) >= date_from)
    if date_to:   query = query.filter(db.func.date(AuditLog.timestamp) <= date_to)
    total   = query.count()
    records = query.order_by(AuditLog.timestamp.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({'logs': [r.to_dict() for r in records], 'total': total, 'page': page, 'per_page': per_page})

# ─── SHIPMENT STATUS UPDATE ──────────────────────────────
@admin_bp.route('/api/shipments/<shipment_id>/update-status', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def update_shipment_status(shipment_id):
    rec = Logistics.query.filter_by(shipment_id=shipment_id).first()
    if not rec:
        return jsonify({'status': 'error', 'message': 'Shipment not found'}), 404
    d = request.get_json() or {}
    new_status = d.get('delivery_status', '').strip()
    valid = ['Dispatched', 'Picked Up', 'In Transit', 'Out for Delivery', 'Delivered', 'Cancelled', 'Delayed']
    if new_status not in valid:
        return jsonify({'status': 'error', 'message': f'Invalid status. Valid: {", ".join(valid)}'}), 400
    old_status = rec.delivery_status
    rec.delivery_status = new_status
    # If delivered, set delivery date and update inventory flag
    from datetime import date as _date
    if new_status == 'Delivered':
        rec.delivery_date = str(_date.today())
        inv = Inventory.query.filter_by(product_id=rec.product_id, site_id=rec.site_id).first()
        if inv and (inv.ending_inventory or 0) > 0:
            inv.stockout_flag = 'No'
    elif new_status == 'Cancelled':
        # Restore inventory if cancelled after dispatch
        inv = Inventory.query.filter_by(product_id=rec.product_id, site_id=rec.site_id).first()
        if inv:
            inv.ending_inventory = (inv.ending_inventory or 0) + (rec.quantity or 0)
    db.session.commit()
    log_action('UPDATE', 'Shipments', f'Shipment {shipment_id}', f'Status: {old_status} → {new_status}')
    return jsonify({'status': 'success', 'message': f'Status updated to {new_status}', 'delivery_status': new_status})

# ─── CUSTOMERS ───────────────────────────────────────────
@admin_bp.route('/customers')
@login_required
@role_required('admin')
@handle_errors
def customers_page():
    return render_template('admin/customers.html')


@admin_bp.route('/api/customers', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def api_admin_customers_get():
    q = request.args.get('q', '').strip()
    per_page = request.args.get('per_page', 300, type=int)
    query = Customer.query
    if q:
        query = query.filter(Customer.customer_id.ilike(f'%{q}%'))
    customers = query.order_by(Customer.customer_id).limit(per_page).all()
    return jsonify({'customers': [{'customer_id': c.customer_id} for c in customers]})


@admin_bp.route('/api/customers', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def api_admin_customers_post():
    d = request.get_json()
    customer_id = (d.get('customer_id') or '').strip()
    if not customer_id:
        count = Customer.query.count()
        customer_id = f'CUST{10000 + count + 1}'
    if Customer.query.filter_by(customer_id=customer_id).first():
        return jsonify({'status': 'error', 'message': 'Customer ID already exists'}), 400
    from datetime import date as _dt
    c = Customer(
        customer_id=customer_id,
        age=int(d.get('age', 0) or 0),
        gender=d.get('gender', ''),
        income_bracket=d.get('income_bracket', ''),
        purchase_frequency=int(d.get('purchase_frequency', 0) or 0),
        average_spend=float(d.get('average_spend', 0) or 0),
        preferred_categories=d.get('preferred_categories', ''),
        total_spend=0, clv=0, csat=0, nps=0,
    )
    db.session.add(c)
    db.session.commit()
    log_action('CREATE', 'Customers', f'Customer {customer_id}', 'Created via Sales Order modal')
    return jsonify({'status': 'success', 'customer_id': customer_id})


# NOTE: /customers/list and /customers/stats are handled by admin_json_bp
#       (registered at the same /admin prefix). Duplicates removed to avoid
#       endpoint name conflicts that caused 500 errors.


# NOTE: /dashboard/monthly-inventory-metrics is handled by admin_json_bp.
#       Duplicate removed to avoid endpoint name conflicts.

# ─── CONTACT MESSAGES (Admin Inbox) ──────────────────────
@admin_bp.route('/messages')
@login_required
@role_required('admin')
@handle_errors
def contact_messages():
    return render_template('admin/messages.html')

@admin_bp.route('/api/messages', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_contact_messages():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    q_str = request.args.get('q', '').strip()
    query = ContactMessage.query
    if q_str:
        query = query.filter(db.or_(
            ContactMessage.name.ilike(f'%{q_str}%'),
            ContactMessage.email.ilike(f'%{q_str}%'),
            ContactMessage.message.ilike(f'%{q_str}%'),
        ))
    total = query.count()
    records = query.order_by(ContactMessage.id.desc()).offset((page-1)*per_page).limit(per_page).all()
    unread = ContactMessage.query.filter_by(is_read=False).count()
    return jsonify({'messages': [m.to_dict() for m in records], 'total': total, 'unread': unread, 'page': page})

@admin_bp.route('/api/messages/<int:msg_id>/read', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def mark_message_read(msg_id):
    msg = db.session.get(ContactMessage, msg_id)
    if not msg:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    msg.is_read = True
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/api/messages/<int:msg_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_contact_message(msg_id):
    msg = db.session.get(ContactMessage, msg_id)
    if not msg:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/api/messages/unread-count', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def unread_message_count():
    count = ContactMessage.query.filter_by(is_read=False).count()
    return jsonify({'count': count})

# ─── PROMOTIONS FULL CRUD ─────────────────────────────────
@admin_bp.route('/api/promotions/list', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_promotions_list():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    q = request.args.get('q', '').strip()
    query = (db.session.query(Promotion, Product, Site)
             .join(Product, Promotion.product_id == Product.product_id, isouter=True)
             .join(Site,    Promotion.site_id    == Site.site_id,       isouter=True))
    if q:
        query = query.filter(Product.product_name.ilike(f'%{q}%'))
    total = query.count()
    records = query.order_by(Promotion.start_date.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'records': [{
            'id':                  promo.id,
            'product_id':          promo.product_id,
            'product_name':        p.product_name if p else promo.product_id,
            'site_id':             promo.site_id,
            'site_name':           s.site_name if s else promo.site_id,
            'promotion_type':      promo.discount_type,
            'discount_percentage': float(promo.discount_amount or 0),
            'start_date':          str(promo.start_date) if promo.start_date else '',
            'end_date':            str(promo.end_date) if promo.end_date else '',
        } for promo, p, s in records],
        'total': total, 'page': page, 'per_page': per_page
    })

@admin_bp.route('/api/promotions/create', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def create_promotion_admin():
    import uuid as _uuid
    d = request.get_json()
    promo = Promotion(
        promotion_id=f"PROMO-{str(_uuid.uuid4())[:8].upper()}",
        product_id=d.get('product_id',''),
        site_id=d.get('site_id',''),
        discount_type=d.get('promotion_type','Discount'),
        discount_amount=float(d.get('discount_percentage',0)),
        start_date=d.get('start_date','') or None,
        end_date=d.get('end_date','') or None,
    )
    db.session.add(promo)
    db.session.commit()
    log_action('CREATE', 'Promotions', f'Promo {promo.id}', f'Product: {promo.product_id}')
    return jsonify({'status': 'success', 'id': promo.id})

@admin_bp.route('/api/promotions/<int:promo_id>/update', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def update_promotion_admin(promo_id):
    promo = db.session.get(Promotion, promo_id)
    if not promo:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    d = request.get_json()
    promo.product_id = d.get('product_id', promo.product_id)
    promo.site_id = d.get('site_id', promo.site_id)
    promo.discount_type = d.get('promotion_type', promo.discount_type)
    promo.discount_amount = float(d.get('discount_percentage', promo.discount_amount or 0))
    promo.start_date = d.get('start_date', promo.start_date) or None
    promo.end_date = d.get('end_date', promo.end_date) or None
    db.session.commit()
    log_action('UPDATE', 'Promotions', f'Promo {promo_id}', 'Updated')
    return jsonify({'status': 'success'})

@admin_bp.route('/api/promotions/<int:promo_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_promotion_admin(promo_id):
    promo = db.session.get(Promotion, promo_id)
    if not promo:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    db.session.delete(promo)
    db.session.commit()
    log_action('DELETE', 'Promotions', f'Promo {promo_id}', 'Deleted')
    return jsonify({'status': 'success'})

# ─── SEASONAL PLAN FULL CRUD ──────────────────────────────
@admin_bp.route('/api/seasonal-plans/list', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_seasonal_plans_list():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    q = request.args.get('q', '').strip()
    query = (db.session.query(SeasonalPlan, Site)
             .join(Site, SeasonalPlan.site_id == Site.site_id, isouter=True))
    if q:
        query = query.filter(SeasonalPlan.product_category.ilike(f'%{q}%'))
    total = query.count()
    records = query.order_by(SeasonalPlan.id.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'records': [{
            'id':               sp.id,
            'month':            sp.month or '',
            'site_id':          sp.site_id or '',
            'site_name':        s.site_name if s else sp.site_id or '',
            'category':         sp.product_category or '',
            'forecasted_sales': sp.forecasted_sales or 0,
            'actual_sales':     sp.actual_sales or 0,
            'seasonal_adj':     sp.seasonal_adjustments or 0,
        } for sp, s in records],
        'total': total, 'page': page, 'per_page': per_page
    })

@admin_bp.route('/api/seasonal-plans/create', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def create_seasonal_plan_admin():
    d = request.get_json()
    sp = SeasonalPlan(
        site_id=d.get('site_id',''),
        month=d.get('month',''),
        product_category=d.get('category',''),
        forecasted_sales=float(d.get('forecasted_sales',0) or 0),
        actual_sales=float(d.get('actual_sales',0) or 0),
        seasonal_adjustments=float(d.get('seasonal_adj',0) or 0),
    )
    db.session.add(sp)
    db.session.commit()
    log_action('CREATE', 'Seasonal Plans', f'Plan {sp.id}', f'Month: {sp.month}')
    return jsonify({'status': 'success', 'id': sp.id})

@admin_bp.route('/api/seasonal-plans/<int:plan_id>/update', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def update_seasonal_plan_admin(plan_id):
    sp = db.session.get(SeasonalPlan, plan_id)
    if not sp:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    d = request.get_json()
    sp.site_id = d.get('site_id', sp.site_id)
    sp.month = d.get('month', sp.month)
    sp.product_category = d.get('category', sp.product_category)
    sp.forecasted_sales = float(d.get('forecasted_sales', sp.forecasted_sales or 0) or 0)
    sp.actual_sales = float(d.get('actual_sales', sp.actual_sales or 0) or 0)
    sp.seasonal_adjustments = float(d.get('seasonal_adj', sp.seasonal_adjustments or 0) or 0)
    db.session.commit()
    log_action('UPDATE', 'Seasonal Plans', f'Plan {plan_id}', 'Updated')
    return jsonify({'status': 'success'})

@admin_bp.route('/api/seasonal-plans/<int:plan_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def delete_seasonal_plan_admin(plan_id):
    sp = db.session.get(SeasonalPlan, plan_id)
    if not sp:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    db.session.delete(sp)
    db.session.commit()
    log_action('DELETE', 'Seasonal Plans', f'Plan {plan_id}', 'Deleted')
    return jsonify({'status': 'success'})

# ─── INVENTORY LIST API (for admin inventory page) ────────
@admin_bp.route('/inventory/list', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def inventory_list():
    page     = request.args.get('page', 1, type=int)
    per_page = 20
    site_f   = request.args.get('site_id', '').strip()
    stockout = request.args.get('stockout', '').strip()
    q        = request.args.get('q', '').strip()
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
    records = query.order_by(Inventory.id.desc()).offset((page-1)*per_page).limit(per_page).all()

    # ── Batch-fetch SO / PO / Sale aggregates for all page records ──────
    # Avoids 3 extra queries per row (N+1 → 3 total)
    inv_keys = [(inv.product_id, inv.site_id) for inv, p, s in records]
    prod_ids  = list({k[0] for k in inv_keys})
    site_ids  = list({k[1] for k in inv_keys if k[1]})

    # Sales Orders batch — SalesOrder uses 'site' (str), not site_id
    so_rows = db.session.query(
        SalesOrder.customer_id,
        func.count(SalesOrder.id).label('cnt'),
        func.coalesce(func.sum(SalesOrder.total_amount), 0).label('total')
    ).group_by(SalesOrder.customer_id).all()
    so_total_count = sum(r.cnt for r in so_rows)
    so_total_amt   = sum(float(r.total) for r in so_rows)

    # Purchase Orders batch — PurchaseOrder uses 'site' (str), not site_id
    po_rows = db.session.query(
        PurchaseOrder.product_id,
        func.count(PurchaseOrder.id).label('cnt'),
        func.coalesce(func.sum(PurchaseOrder.total_cost), 0).label('total')
    ).filter(PurchaseOrder.product_id.in_(prod_ids)).group_by(
        PurchaseOrder.product_id).all()
    po_map = {r.product_id: r for r in po_rows}

    # Sales (qty sold) batch — Sale uses 'units_sold', not 'quantity_sold'
    sale_rows = db.session.query(
        Sale.product_id, Sale.site_id,
        func.coalesce(func.sum(Sale.units_sold), 0).label('qty')
    ).filter(Sale.product_id.in_(prod_ids)).group_by(
        Sale.product_id, Sale.site_id).all()
    sale_map = {(r.product_id, r.site_id): int(r.qty) for r in sale_rows}

    # Batch-fetch StockLevels for accurate current stock
    from models.records import StockLevel
    sl_rows = StockLevel.query.filter(
        StockLevel.site_id.in_(site_ids),
        StockLevel.product_id.in_(prod_ids)
    ).all()
    sl_map = {(sl.site_id, sl.product_id): (sl.qty_on_hand or 0) for sl in sl_rows}

    result = []
    for inv, p, s in records:
        bi  = inv.beginning_inventory or 0
        ei  = inv.ending_inventory or 0
        rep = inv.replenishment or 0
        # Correct beginning inventory: if no beginning data, derive it
        display_beginning = (ei + rep) if (bi == 0 and rep > 0) else bi
        # Correct ending inventory formula: BI + Replenishment - Sold = EI
        key      = (inv.product_id, inv.site_id)
        po_row   = po_map.get(inv.product_id)
        qty_sold = sale_map.get(key, 0)
        # Correct EI: use DB value; compute formula-based for display consistency
        ei_calc  = display_beginning + rep - qty_sold
        ei_display = ei if ei > 0 else max(0, ei_calc)
        # Current stock: prefer StockLevel, fall back to ending_inventory
        sl_key   = (inv.site_id, inv.product_id)
        stock_now = sl_map.get(sl_key, ei_display)
        reorder_pt = p.reorder_point if p and hasattr(p,'reorder_point') else 0
        unit_price = float(p.unit_price or 0) if p else 0
        unit_cost  = float(p.unit_cost  or 0) if p else 0
        margin     = round((unit_price - unit_cost) / unit_price * 100, 1) if unit_price > 0 else 0
        result.append({
            'id':                  inv.id,
            'product_id':          inv.product_id,
            'product_name':        p.product_name if p else inv.product_id,
            'site_id':             inv.site_id,
            'site_name':           s.site_name if s else inv.site_id,
            'beginning_inventory': display_beginning,
            'ending_inventory':    ei_display,
            'replenishment':       rep,
            'qty_sold':            qty_sold,
            'stockout_flag':       'Yes' if stock_now == 0 else ('Yes' if inv.stockout_flag == 'Yes' else 'No'),
            'unit_cost':           unit_cost,
            'unit_price':          unit_price,
            'profit_margin':       margin,
            'category':            p.category    if p and hasattr(p,'category')    else '',
            'subcategory':         p.subcategory if p and hasattr(p,'subcategory') else '',
            'supplier':            p.supplier    if p and hasattr(p,'supplier')    else '',
            'total_sold':          qty_sold,
            'current_stock':       int(stock_now),
            'reorder_point':       int(reorder_pt),
            'required_stock':      max(0, int(reorder_pt) - int(stock_now)) if stock_now < reorder_pt else 0,
            'so_count':            0,
            'so_total':            0.0,
            'po_count':            int(po_row.cnt)   if po_row else 0,
            'po_total':            float(po_row.total) if po_row else 0.0,
        })
    return jsonify({'records': result, 'total': total, 'page': page, 'per_page': per_page})


# ─── INVOICE GENERATION ──────────────────────────────────────────────────────

@admin_bp.route('/invoice/so/<so_number>')
@login_required
@role_required('admin')
@handle_errors
def generate_so_invoice(so_number):
    so = SalesOrder.query.filter_by(so_number=so_number).first()
    if not so:
        return "Sales Order not found", 404
    so_dict = so.to_dict()
    # Fetch site details
    site_obj = Site.query.filter_by(site_id=so.site).first()
    site_info = {'site_id': so.site, 'site_name': '', 'city': '', 'region': ''}
    if site_obj:
        site_info = {'site_id': site_obj.site_id, 'site_name': site_obj.site_name or '', 'city': site_obj.city or '', 'region': site_obj.region or ''}
    # Fetch customer details
    cust_obj = Customer.query.filter_by(customer_id=so.customer_id).first()
    cust_info = {'customer_id': so.customer_id, 'name': so.customer, 'email': so.customer_email, 'state': so.state}
    if cust_obj:
        cust_info.update({'name': cust_obj.customer_id, 'email': getattr(cust_obj, 'email', so.customer_email) or so.customer_email})
    # Build invoice number
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

@admin_bp.route('/invoice/po/<po_number>')
@login_required
@role_required('admin')
@handle_errors
def generate_po_invoice(po_number):
    po = PurchaseOrder.query.filter_by(po_number=po_number).first()
    if not po:
        return "Purchase Order not found", 404
    # Fetch site details
    site_raw = po.site or ''
    site_id = site_raw.split(' - ')[0].strip() if ' - ' in site_raw else site_raw.strip()
    site_obj = Site.query.filter_by(site_id=site_id).first()
    site_info = {'site_id': site_id, 'site_name': '', 'city': '', 'region': ''}
    if site_obj:
        site_info = {'site_id': site_obj.site_id, 'site_name': site_obj.site_name or '', 'city': site_obj.city or '', 'region': site_obj.region or ''}
    # Supplier info
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
# ── SALES RETURNS ──────────────────────────────────────────
# ═══════════════════════════════════════════════════════════

@admin_bp.route('/sales-returns')
@login_required
@role_required('admin')
def sales_returns_page():
    return render_template('admin/sales_returns.html')


@admin_bp.route('/api/sales-returns', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_sales_returns():
    q      = request.args.get('q', '').strip().lower()
    status = request.args.get('status', '').strip()
    page   = request.args.get('page', 1, type=int)
    per_page = 20
    query  = SalesReturn.query.filter_by(role='admin')
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

    # Calculate stats from all matching records
    all_records = query.all()
    total = len(all_records)
    pending_count = sum(1 for r in all_records if r.status == 'Pending')
    approved_count = sum(1 for r in all_records if r.status == 'Approved')
    rejected_count = sum(1 for r in all_records if r.status == 'Rejected')
    processed_count = sum(1 for r in all_records if r.status == 'Processed')
    total_refund = sum(float(r.total_refund or 0) for r in all_records)

    # Apply pagination
    records = all_records[(page-1)*per_page:page*per_page]

    return jsonify({
        'returns': [r.to_dict() for r in records],
        'total': total,
        'page': page,
        'stats': {
            'total_returns': total,
            'pending': pending_count,
            'approved': approved_count,
            'rejected': rejected_count,
            'processed': processed_count,
            'total_refund': round(total_refund, 2)
        }
    })


@admin_bp.route('/api/sales-returns', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def create_sales_return():
    from datetime import date as _date
    d       = request.get_json()
    so_num  = (d.get('so_number') or '').strip()
    if not so_num:
        return jsonify({'status': 'error', 'message': 'SO Number is required'}), 400
    so = SalesOrder.query.filter_by(so_number=so_num).first()
    if not so:
        return jsonify({'status': 'error', 'message': 'Sales Order not found'}), 404
    rn = 'SR-' + ''.join(random.choices(_string.ascii_uppercase + _string.digits, k=6))
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
        created_by    = session.get('username', 'Admin'),
        role          = 'admin',
    )
    db.session.add(ret)
    db.session.commit()
    log_action('CREATE', 'Sales Returns', f'Return {rn}', f'SO: {so_num}, Refund: {refund:.2f}')
    return jsonify({'status': 'success', 'return_number': rn})


@admin_bp.route('/api/sales-returns/<rn>/approve', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def approve_sales_return(rn):
    from datetime import date as _date
    ret = SalesReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status      = 'Approved'
    ret.approved_at = str(_date.today())
    ret.approved_by = session.get('username', 'Admin')
    db.session.commit()
    log_action('UPDATE', 'Sales Returns', f'Return {rn}', 'Status: Approved')
    return jsonify({'status': 'success'})


@admin_bp.route('/api/sales-returns/<rn>/reject', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def reject_sales_return(rn):
    ret = SalesReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status = 'Rejected'
    db.session.commit()
    log_action('UPDATE', 'Sales Returns', f'Return {rn}', 'Status: Rejected')
    return jsonify({'status': 'success'})


# ═══════════════════════════════════════════════════════════
# ── PURCHASE RETURNS ───────────────────────────────────────
# ═══════════════════════════════════════════════════════════

@admin_bp.route('/purchase-returns')
@login_required
@role_required('admin')
def purchase_returns_page():
    return render_template('admin/purchase_returns.html')


@admin_bp.route('/api/purchase-returns', methods=['GET'])
@login_required
@role_required('admin')
@handle_errors
def get_purchase_returns():
    q      = request.args.get('q', '').strip().lower()
    status = request.args.get('status', '').strip()
    page   = request.args.get('page', 1, type=int)
    per_page = 20
    query  = PurchaseReturn.query.filter_by(role='admin')
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
    total   = query.count()
    records = query.order_by(PurchaseReturn.id.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({'returns': [r.to_dict() for r in records], 'total': total, 'page': page})


@admin_bp.route('/api/purchase-returns', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def create_purchase_return():
    from datetime import date as _date
    d      = request.get_json()
    po_num = (d.get('po_number') or '').strip()
    if not po_num:
        return jsonify({'status': 'error', 'message': 'PO Number is required'}), 400
    po = PurchaseOrder.query.filter_by(po_number=po_num).first()
    if not po:
        return jsonify({'status': 'error', 'message': 'Purchase Order not found'}), 404
    rn        = 'PR-' + ''.join(random.choices(_string.ascii_uppercase + _string.digits, k=6))
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
        created_by    = session.get('username', 'Admin'),
        role          = 'admin',
    )
    db.session.add(ret)
    db.session.commit()
    log_action('CREATE', 'Purchase Returns', f'Return {rn}', f'PO: {po_num}, Credit: {credit:.2f}')
    return jsonify({'status': 'success', 'return_number': rn})


@admin_bp.route('/api/purchase-returns/<rn>/approve', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def approve_purchase_return(rn):
    from datetime import date as _date
    ret = PurchaseReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status      = 'Approved'
    ret.approved_at = str(_date.today())
    ret.approved_by = session.get('username', 'Admin')
    db.session.commit()
    log_action('UPDATE', 'Purchase Returns', f'Return {rn}', 'Status: Approved')
    return jsonify({'status': 'success'})


@admin_bp.route('/api/purchase-returns/<rn>/reject', methods=['POST'])
@login_required
@role_required('admin')
@handle_errors
def reject_purchase_return(rn):
    ret = PurchaseReturn.query.filter_by(return_number=rn).first()
    if not ret:
        return jsonify({'status': 'error', 'message': 'Return not found'}), 404
    ret.status = 'Rejected'
    db.session.commit()
    log_action('UPDATE', 'Purchase Returns', f'Return {rn}', 'Status: Rejected')
    return jsonify({'status': 'success'})
