"""
ChatHistory Model
Stores all user-AI conversation history
"""

from datetime import datetime
from extensions import db


class ChatHistory(db.Model):
    """Model to persist all chatbot conversations"""
    
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(50), default='general', nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    severity = db.Column(db.String(20), default='low')  # low, medium, high, critical
    session_id = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # ML Feedback
    template_idx = db.Column(db.Integer, default=0)
    feedback_rating = db.Column(db.Float, nullable=True)  # User rating for ML feedback loop

    
    def to_dict(self) -> dict:
        """Serialize chat history entry"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'intent': self.intent,
            'confidence': round(self.confidence, 3),
            'severity': self.severity,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }
    
    @staticmethod
    def get_intent_stats() -> list:
        """Get aggregated intent statistics for analytics"""
        from sqlalchemy import func
        return db.session.query(
            ChatHistory.intent,
            func.count(ChatHistory.id).label('count')
        ).group_by(ChatHistory.intent).all()
    
    @staticmethod
    def get_daily_activity(days: int = 7) -> list:
        """Get daily chat activity for past N days"""
        from sqlalchemy import func, cast, Date
        from datetime import datetime, timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        return db.session.query(
            func.date(ChatHistory.timestamp).label('date'),
            func.count(ChatHistory.id).label('count')
        ).filter(ChatHistory.timestamp >= cutoff)\
         .group_by(func.date(ChatHistory.timestamp))\
         .order_by(func.date(ChatHistory.timestamp)).all()
    
    def __repr__(self):
        return f'<ChatHistory user={self.user_id} intent={self.intent}>'
