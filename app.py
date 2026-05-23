"""
SmartAssist: AI-Powered Disaster Management Support System
Main Flask Application Entry Point

Author: SmartAssist Dev Team
Version: 1.0.0
"""

import eventlet
eventlet.monkey_patch()

import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template
from config import config
from extensions import db, login_manager
from models.user import User


def create_app(config_name: str = 'default') -> Flask:
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Apply ProxyFix to support SSL termination behind reverse proxies (like Hugging Face)
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    
    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Initialize SocketIO, JWT, Limiter, and Mail
    from extensions import socketio, jwt, limiter, mail
    socketio.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.chat import chat_bp
    from routes.admin import admin_bp
    from routes.analytics import analytics_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)
    
    # Template context processors
    @app.context_processor
    def inject_globals():
        return {
            'app_name': app.config.get('APP_NAME', 'SmartAssist'),
            'version': app.config.get('VERSION', '1.0.0'),
            'current_year': datetime.now().year
        }
    
    # Custom error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html', code=404, message='Page Not Found'), 404
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', code=403, message='Access Forbidden'), 403
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('error.html', code=500, message='Internal Server Error'), 500
    
    # Initialize database and seed data
    with app.app_context():
        db.create_all()
        _seed_initial_data(app)
    
    return app


def _seed_initial_data(app: Flask):
    """
    Seed initial data: admin user and sample emergency reports.
    Only runs if the database is empty.
    """
    from models.user import User
    from models.reports import EmergencyReport
    from models.chat import ChatHistory
    from models.admin_logs import AdminLog
    
    # Create admin user if not exists
    admin_email = app.config['ADMIN_EMAIL']
    admin = User.query.filter_by(email=admin_email).first()
    
    if not admin:
        admin = User(
            name='System Administrator',
            email=admin_email,
            role='admin',
            is_active=True
        )
        admin.set_password(app.config['ADMIN_PASSWORD'])
        db.session.add(admin)
        db.session.flush()  # Get admin.id before commit
        
        # Seed sample emergency reports
        sample_reports = [
            EmergencyReport(user_id=admin.id, disaster_type='Flood Emergency',
                          location='Mumbai', severity='high', status='resolved',
                          description='Flash flood in low-lying areas', is_escalated=True),
            EmergencyReport(user_id=admin.id, disaster_type='Fire Emergency',
                          location='Delhi', severity='critical', status='in_progress',
                          description='Building fire requiring evacuation', is_escalated=True),
            EmergencyReport(user_id=admin.id, disaster_type='Earthquake Help',
                          location='Gujarat', severity='medium', status='open',
                          description='Minor tremors causing structural concerns'),
            EmergencyReport(user_id=admin.id, disaster_type='Cyclone Emergency',
                          location='Chennai', severity='high', status='resolved',
                          description='Cyclone warning issued for coastal areas', is_escalated=True),
        ]
        
        # Seed sample chat history
        sample_chats = [
            ChatHistory(user_id=admin.id, user_message='There is a flood near my house',
                       bot_response='Move to higher ground immediately...', intent='flood_emergency',
                       confidence=0.92, severity='high'),
            ChatHistory(user_id=admin.id, user_message='Fire in my building',
                       bot_response='Evacuate immediately...', intent='fire_emergency',
                       confidence=0.95, severity='critical'),
            ChatHistory(user_id=admin.id, user_message='Where can I find shelter?',
                       bot_response='Contact local disaster relief...', intent='shelter_request',
                       confidence=0.87, severity='medium'),
            ChatHistory(user_id=admin.id, user_message='What is the emergency number?',
                       bot_response='National Emergency: 112...', intent='emergency_contact',
                       confidence=0.91, severity='low'),
            ChatHistory(user_id=admin.id, user_message='Earthquake hit our area',
                       bot_response='Drop, Cover, Hold On...', intent='earthquake_help',
                       confidence=0.89, severity='high'),
        ]
        
        # Admin log entry
        log = AdminLog(
            admin_id=admin.id,
            action='System initialized',
            details='SmartAssist platform initialized with admin account'
        )
        
        db.session.add_all(sample_reports + sample_chats + [log])
        db.session.commit()
        
        app.logger.info(f"✅ Admin user created: {admin_email}")
        app.logger.info("✅ Sample data seeded successfully")


# Application entry point
if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("\n" + "="*60)
    print("  SmartAssist - AI Disaster Management System")
    print("="*60)
    print(f"  URL: http://localhost:5000")
    print(f"  Admin: admin@smartassist.com / Admin@123")
    print(f"  Analytics: http://localhost:5000/analytics")
    print(f"  Chatbot: http://localhost:5000/chatbot")
    print("="*60 + "\n")
    
    from extensions import socketio
    socketio.run(
        app,
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
