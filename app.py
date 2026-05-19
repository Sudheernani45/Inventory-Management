from flask import Flask, session, jsonify, redirect
from config import config
from models.db import db
from extensions import mail
from flask_migrate import Migrate

from routes.admin_routes      import admin_bp
from routes.admin_json_routes import admin_json_bp
from routes.api_routes        import api_bp
from routes.auth_routes       import auth_bp
from routes.common_routes     import common_bp
from routes.manager_routes    import manager_bp
from routes.analyst_routes    import analyst_bp
from routes.supplier_routes   import supplier_bp   # ← ADDED

migrate = Migrate()


def _safe_migrate(app):
    """
    Zero-downtime column additions.
    Uses ALTER TABLE … ADD COLUMN IF NOT EXISTS so re-running is always safe.
    Called once inside create_app() after db.create_all().
    """
    with app.app_context():
        engine = db.engine
        with engine.connect() as conn:
            stmts = [
                # users — new profile fields
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS department VARCHAR(100)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS employee_id VARCHAR(50) UNIQUE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS photo_url VARCHAR(500)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()",
                # products — new catalogue fields
                "ALTER TABLE products ADD COLUMN IF NOT EXISTS uom VARCHAR(30) DEFAULT 'Unit'",
                "ALTER TABLE products ADD COLUMN IF NOT EXISTS reorder_point INTEGER DEFAULT 0",
                "ALTER TABLE products ADD COLUMN IF NOT EXISTS reorder_qty INTEGER DEFAULT 0",
                "ALTER TABLE products ADD COLUMN IF NOT EXISTS default_warehouse VARCHAR(20)",
                "ALTER TABLE products ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'Active'",
                "ALTER TABLE products ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()",
                "ALTER TABLE products ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()",
                # suppliers — extended profile
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS address TEXT",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS contact_person VARCHAR(150)",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS category VARCHAR(100)",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'Active'",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS notes TEXT",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()",
                # sales_orders — workflow + tracking fields
                "ALTER TABLE sales_orders ADD COLUMN IF NOT EXISTS customer_id VARCHAR(50) DEFAULT ''",
                "ALTER TABLE sales_orders ADD COLUMN IF NOT EXISTS customer_email VARCHAR(120) DEFAULT ''",
                "ALTER TABLE sales_orders ADD COLUMN IF NOT EXISTS notes TEXT DEFAULT ''",
                "ALTER TABLE sales_orders ADD COLUMN IF NOT EXISTS cancelled_at VARCHAR(20) DEFAULT ''",
                "ALTER TABLE sales_orders ADD COLUMN IF NOT EXISTS cancel_reason TEXT DEFAULT ''",
                # purchase_orders — workflow + supplier token fields
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS notes TEXT DEFAULT ''",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS rejection_reason TEXT DEFAULT ''",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS received_at VARCHAR(20) DEFAULT ''",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS cancelled_at VARCHAR(20) DEFAULT ''",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS cancel_reason TEXT DEFAULT ''",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS supplier_id INTEGER REFERENCES suppliers(id)",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS supplier_approval_token VARCHAR(128) UNIQUE",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS supplier_token_expiry TIMESTAMP",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS supplier_action VARCHAR(20)",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS supplier_actioned_at TIMESTAMP",
                "ALTER TABLE purchase_orders ADD COLUMN IF NOT EXISTS supplier_reject_reason TEXT",
                # logistics — SO link + tracking fields
                "ALTER TABLE logistics ADD COLUMN IF NOT EXISTS so_id INTEGER REFERENCES sales_orders(id)",
                "ALTER TABLE logistics ADD COLUMN IF NOT EXISTS so_number VARCHAR(50)",
                "ALTER TABLE logistics ADD COLUMN IF NOT EXISTS estimated_delivery DATE",
                "ALTER TABLE logistics ADD COLUMN IF NOT EXISTS tracking_status_updated TIMESTAMP",
                "ALTER TABLE logistics ADD COLUMN IF NOT EXISTS tracking_notes TEXT",
                # sales_returns table
                """CREATE TABLE IF NOT EXISTS sales_returns (
                    id SERIAL PRIMARY KEY,
                    return_number VARCHAR(50) UNIQUE NOT NULL,
                    so_number VARCHAR(50) NOT NULL DEFAULT '',
                    customer VARCHAR(150) DEFAULT '',
                    site VARCHAR(50) DEFAULT '',
                    return_reason TEXT DEFAULT '',
                    items_json TEXT DEFAULT '[]',
                    total_refund FLOAT DEFAULT 0,
                    status VARCHAR(30) DEFAULT 'Pending',
                    notes TEXT DEFAULT '',
                    created_at VARCHAR(20) DEFAULT '',
                    created_by VARCHAR(80) DEFAULT '',
                    approved_at VARCHAR(20) DEFAULT '',
                    approved_by VARCHAR(80) DEFAULT '',
                    role VARCHAR(20) DEFAULT 'admin',
                    manager_user_id INTEGER DEFAULT 0
                )""",
                # purchase_returns table
                """CREATE TABLE IF NOT EXISTS purchase_returns (
                    id SERIAL PRIMARY KEY,
                    return_number VARCHAR(50) UNIQUE NOT NULL,
                    po_number VARCHAR(50) NOT NULL DEFAULT '',
                    supplier VARCHAR(150) DEFAULT '',
                    site VARCHAR(50) DEFAULT '',
                    return_reason TEXT DEFAULT '',
                    product_name VARCHAR(200) DEFAULT '',
                    product_id VARCHAR(50) DEFAULT '',
                    quantity INTEGER DEFAULT 0,
                    unit_cost FLOAT DEFAULT 0,
                    total_credit FLOAT DEFAULT 0,
                    status VARCHAR(30) DEFAULT 'Pending',
                    notes TEXT DEFAULT '',
                    created_at VARCHAR(20) DEFAULT '',
                    created_by VARCHAR(80) DEFAULT '',
                    approved_at VARCHAR(20) DEFAULT '',
                    approved_by VARCHAR(80) DEFAULT '',
                    role VARCHAR(20) DEFAULT 'admin',
                    manager_user_id INTEGER DEFAULT 0
                )""",
            ]
            for stmt in stmts:
                try:
                    conn.execute(db.text(stmt))
                except Exception as e:
                    print(f"[safe_migrate] skip: {e}")
            conn.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Import all models so SQLAlchemy detects all tables
    from models import records
    from models import managers
    from models import user

    with app.app_context():
        db.create_all()        # create missing tables
        _safe_migrate(app)     # add missing columns to existing tables

    # Register blueprints
    app.register_blueprint(common_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp,      url_prefix='/admin')
    app.register_blueprint(admin_json_bp, url_prefix='/admin')
    app.register_blueprint(manager_bp,    url_prefix='/manager')
    app.register_blueprint(analyst_bp,    url_prefix='/analyst')
    app.register_blueprint(supplier_bp)   # url_prefix='/supplier' set in blueprint

    # /api/me — returns current logged-in user info
    @app.route('/api/me')
    def api_me():
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        from models.user import User
        u = db.session.get(User, session['user_id'])
        if not u:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            'id':          u.id,
            'name':        u.name,
            'email':       u.email,
            'role':        u.role,
            'is_active':   getattr(u, 'is_active', True),
            'employee_id': getattr(u, 'employee_id', None),
            'photo_url':   getattr(u, 'photo_url', None),
        })

    # ─── Global error handlers ───────────────────────────────────────────────
    # ── Favicon ──────────────────────────────────────────────────────────────
    @app.route('/favicon.ico')
    def favicon():
        from flask import send_from_directory
        import os
        static_dir = os.path.join(app.root_path, 'static')
        if os.path.exists(os.path.join(static_dir, 'favicon.ico')):
            return send_from_directory(static_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
        return '', 204   # No content — suppresses browser 500

    @app.errorhandler(403)
    def forbidden(e):
        role = session.get('role', '')
        if not role or 'user_id' not in session:
            return redirect('/login')
        if role == 'admin':
            return redirect('/admin/dashboard')
        elif role == 'manager':
            return redirect('/manager/dashboard')
        elif role == 'analyst':
            return redirect('/analyst/dashboard')
        return redirect('/login')

    @app.errorhandler(404)
    def not_found(e):
        from flask import request as req
        if req.path.startswith('/api/') or req.path.startswith('/admin/api') or req.path.startswith('/manager/api') or req.path.startswith('/analyst/api'):
            return jsonify({'status': 'error', 'message': 'Endpoint not found', 'code': 404}), 404
        role = session.get('role', '')
        if role == 'admin':
            return redirect('/admin/dashboard')
        elif role == 'manager':
            return redirect('/manager/dashboard')
        elif role == 'analyst':
            return redirect('/analyst/dashboard')
        return redirect('/login')

    @app.errorhandler(401)
    def unauthorized(e):
        return redirect('/login')

    # ─── CLI Commands ───────────────────────────────────────────────────────
    @app.cli.command('populate-customer-spend')
    def populate_customer_spend():
        """Calculate and populate total_spend from sales data."""
        from models.populate_customer_spend import populate_customer_metrics
        populate_customer_metrics()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
