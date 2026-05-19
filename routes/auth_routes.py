from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from models.db import db
import traceback
from werkzeug.security import generate_password_hash
import os, random, string
from utils.email import send_credentials_email

auth_bp = Blueprint('auth', __name__)

def random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

# ------------------ DECORATORS ------------------

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_role = session.get('role')
            if user_role not in roles:
                # Not logged in at all -> go to login
                if 'user_id' not in session:
                    return redirect(url_for('auth.login'))
                # Logged in but wrong role -> redirect to their own dashboard
                if user_role == 'admin':
                    return redirect('/admin/dashboard')
                elif user_role == 'manager':
                    return redirect('/manager/dashboard')
                elif user_role == 'analyst':
                    return redirect('/analyst/dashboard')
                # Unknown role
                session.clear()
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ---------------error decorator---------------
def handle_errors(f):
    """Decorator — wraps a route function in try/except"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()          # prints full stack to server console
            return jsonify({
                'status':  'error',
                'message': str(e)
            }), 500
    return wrapper

# ------------------ LOGIN ------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data     = request.get_json()
        email    = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Deactivated accounts cannot log in
            if not getattr(user, 'is_active', True):
                return jsonify({"message": "Your account has been deactivated. Please contact an administrator."}), 403
            session['user_id']  = user.id
            session['role']     = user.role
            session['username'] = user.name
            try:
                from utils.audit import log_action
                log_action('LOGIN', 'Auth', f'User {user.name}', f'Role: {user.role}')
            except Exception: pass

            # First-login password change for all non-admin roles
            if getattr(user, 'is_first_login', False) and user.role != 'admin':
                return jsonify({"redirect": "/change-password"})

            # Role-based dashboard redirect
            if user.role == 'admin':
                return jsonify({"redirect": "/admin/dashboard"})
            elif user.role == 'manager':
                return jsonify({"redirect": "/manager/dashboard"})
            elif user.role == 'analyst':
                return jsonify({"redirect": "/analyst/dashboard"})
            else:
                return jsonify({"redirect": "/login"})

        return jsonify({"message": "Invalid email or password"}), 401

    return render_template('common/login.html')

# ------------------ LOGOUT ------------------

@auth_bp.route('/logout')
def logout():
    try:
        from utils.audit import log_action
        log_action('LOGOUT', 'Auth', f'User {session.get("username","?")}', 'Logged out')
    except Exception: pass
    session.clear()
    return redirect('/login')

# ------------------ CHANGE PASSWORD ------------------

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
@handle_errors
def change_password():
    if request.method == 'POST':
        data         = request.get_json()
        new_password = data.get('password')
        user = db.session.get(User, session['user_id'])
        user.password       = generate_password_hash(new_password)
        user.is_first_login = False
        db.session.commit()
        if user.role == 'admin':
            return jsonify({"message": "Password updated successfully!", "redirect": "/admin/dashboard"})
        elif user.role == 'manager':
            return jsonify({"message": "Password updated successfully!", "redirect": "/manager/dashboard"})
        elif user.role == 'analyst':
            return jsonify({"message": "Password updated successfully!", "redirect": "/analyst/dashboard"})
        return jsonify({"message": "Password updated successfully!", "redirect": "/login"})

    return render_template('auth/change_password.html')

# ------------- forgot password-------------------
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@handle_errors
def forgot_password():

    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'status': 'error', 'message': 'Email does not exist'}), 400

        auto_pwd = random_password().strip()
        user.password = generate_password_hash(auto_pwd)
        user.is_first_login = True
        email_sent = True
        try:
            send_credentials_email(user.email, user.name, auto_pwd)
        except Exception as e:
            print(f'Email error: {e}')
            email_sent = False
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Password sent to email',
            'email_sent': email_sent,
            'redirect': '/login'
        }), 200

    return render_template('common/forgot_password.html')