import pytest
from app import create_app
from extensions import db
from models.user import User

@pytest.fixture
def client():
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(email='test@example.com', name='Test User', role='user', is_active=True)
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        yield client

def test_login(client):
    """Test user login"""
    rv = client.post('/login', data=dict(
        email='test@example.com',
        password='password123'
    ), follow_redirects=True)
    assert b'Dashboard' in rv.data

def test_ai_intent_classifier():
    """Test AI NLP engine accuracy"""
    from ai_engine.intent_classifier import get_classifier
    classifier = get_classifier()
    
    intent, confidence = classifier.classify("There is a massive flood outside my house")
    assert intent == "flood_emergency"
    
    intent, confidence = classifier.classify("Help! My kitchen is on fire!")
    assert intent == "fire_emergency"

def test_ai_response_engine():
    """Test Response Engine generation"""
    from ai_engine.response_engine import get_response_engine
    engine = get_response_engine()
    
    result = engine.generate_response("Where can I find shelter from the flood?")
    assert result['intent'] in ["shelter_request", "flood_emergency"]
    assert "response" in result
    assert "severity" in result
