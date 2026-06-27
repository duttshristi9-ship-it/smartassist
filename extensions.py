"""
Flask Extensions
Centralized initialization of Flask extensions to avoid circular imports
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Database ORM
db = SQLAlchemy()

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# SocketIO for real-time comms
socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')

from flask_mail import Mail

# JWT Manager
jwt = JWTManager()

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# Mail
mail = Mail()
