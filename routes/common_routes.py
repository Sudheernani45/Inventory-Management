from flask import Blueprint, redirect, session, render_template, jsonify, request

common_bp = Blueprint('common', __name__)


@common_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/home')
    role = session.get('role', '')
    if role == 'admin':
        return redirect('/admin/dashboard')
    elif role == 'manager':
        return redirect('/manager/dashboard')
    elif role == 'analyst':
        return redirect('/analyst/dashboard')
    else:
        session.clear()
        return redirect('/login')


def _get_platform_stats():
    """Fetch live stats for static pages."""
    try:
        from models.db import db
        from models.records import Product, Site, Inventory
        from models.user import User
        products  = db.session.query(Product).count()
        sites     = db.session.query(Site).count()
        users     = db.session.query(User).count()
        inventory = db.session.query(Inventory).count()
        in_stock  = db.session.query(Inventory).filter(Inventory.ending_inventory > 10).count()
        low_stock = db.session.query(Inventory).filter(
            Inventory.ending_inventory > 0,
            Inventory.ending_inventory <= 10
        ).count()
        return dict(products=products, sites=sites, users=users,
                    inventory=inventory, in_stock=in_stock, low_stock=low_stock)
    except Exception:
        return dict(products=0, sites=0, users=0, inventory=0, in_stock=0, low_stock=0)


@common_bp.route('/home')
def home():
    stats = _get_platform_stats()
    return render_template('common/home.html', stats=stats)


@common_bp.route('/about')
def about():
    stats = _get_platform_stats()
    return render_template('common/about.html', stats=stats)


@common_bp.route('/features')
def features():
    stats = _get_platform_stats()
    return render_template('common/features.html', stats=stats)


@common_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    from flask import flash
    from datetime import date as _date
    stats = _get_platform_stats()
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        company = request.form.get('company', '').strip()
        subject = request.form.get('subject', 'General Inquiry').strip()
        message = request.form.get('message', '').strip()
        if name and email and message:
            try:
                from models.db import db
                from models.records import ContactMessage
                msg = ContactMessage(
                    name=name, email=email, company=company,
                    subject=subject, message=message,
                    is_read=False, created_at=str(_date.today())
                )
                db.session.add(msg)
                db.session.commit()
            except Exception as e:
                print(f'Contact save error: {e}')
            flash('Thank you! Your message has been sent. We\'ll get back to you within 24 hours.', 'success')
        else:
            flash('Please fill in all required fields.', 'error')
    return render_template('common/contact.html', stats=stats)


@common_bp.route('/api/platform-stats')
def platform_stats():
    """Public API — returns basic platform statistics for static pages."""
    try:
        from models.db import db
        from models.records import Product, Site, Inventory
        from models.user import User

        products  = db.session.query(Product).count()
        sites     = db.session.query(Site).count()
        users     = db.session.query(User).count()
        inventory = db.session.query(Inventory).count()
        in_stock  = db.session.query(Inventory).filter(Inventory.ending_inventory > 10).count()
        low_stock = db.session.query(Inventory).filter(
            Inventory.ending_inventory > 0,
            Inventory.ending_inventory <= 10
        ).count()

        return jsonify({
            'products':  products,
            'sites':     sites,
            'users':     users,
            'inventory': inventory,
            'in_stock':  in_stock,
            'low_stock': low_stock,
        })
    except Exception as e:
        return jsonify({
            'products':  0,
            'sites':     0,
            'users':     0,
            'inventory': 0,
            'in_stock':  0,
            'low_stock': 0,
        })

@common_bp.route('/api/team-members')
def team_members():
    """Returns ALL users as team members for the About page."""
    try:
        from models.db import db
        from models.user import User
        all_users = User.query.order_by(User.role, User.id).all()
        ROLE_LABELS = {
            'admin':   'System Administrator',
            'manager': 'Site Manager',
            'staff':   'Staff Member',
            'analyst': 'Data Analyst',
        }
        members = []
        for u in all_users:
            parts = u.name.strip().split()
            initials = ''.join(p[0].upper() for p in parts[:2]) if parts else 'U'
            members.append({
                'name':     u.name,
                'initials': initials,
                'role':     ROLE_LABELS.get(u.role, u.role.capitalize()),
                'role_key': u.role,
            })
        return jsonify({'members': members, 'total': len(members)})
    except Exception:
        return jsonify({'members': [
            {'name': 'IFMS Team', 'initials': 'IF', 'role': 'Development Team', 'role_key': 'admin'}
        ], 'total': 1})
