"""
Authentication Routes
Handles user login, registration, and logout
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from models.admin_logs import AdminLog

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember-me', False)
        
        # Validate inputs
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=bool(remember))
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Redirect to intended page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            
            if user.is_admin():
                return redirect(url_for('admin.index'))
            return redirect(url_for('dashboard.index'))
        
        flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        errors = []
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters.')
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html', name=name, email=email)
        
        # Check if email exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Create new user
        user = User(name=name, email=email, role='user')
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    from flask import make_response, current_app
    import os
    
    logout_user()
    session.clear()
    
    response = make_response(redirect(url_for('main.landing')))
    
    # Determine security settings dynamically based on env (HTTP vs HTTPS iframe support)
    is_prod = os.environ.get('FLASK_ENV') == 'production' or current_app.config.get('ENV') == 'production'
    
    cookie_options = {
        'path': '/',
        'secure': True if is_prod else False,
        'samesite': 'None' if is_prod else 'Lax'
    }
    
    response.delete_cookie('session', **cookie_options)
    response.delete_cookie('remember_token', **cookie_options)
    
    flash('You have been logged out successfully.', 'info')
    return response
