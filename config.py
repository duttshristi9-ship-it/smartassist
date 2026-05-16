"""
SmartAssist Configuration Module
Manages all application configuration settings
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # Flask secret key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smartassist-disaster-ai-secret-key-2024'
    
    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis & Celery configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
    
    # Application settings
    APP_NAME = "SmartAssist"
    VERSION = "2.0.0" # Upgraded version
    
    # Admin credentials (change in production!)
    ADMIN_EMAIL = "admin@smartassist.com"
    ADMIN_PASSWORD = "Admin@123"
    
    # AI Engine settings
    AI_CONFIDENCE_THRESHOLD = 0.3
    MAX_CHAT_HISTORY = 50  # Messages per session display
    
    # Pagination
    USERS_PER_PAGE = 15
    LOGS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
