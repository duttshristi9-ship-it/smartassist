"""
AdminLog Model
Records all admin actions for audit trail
"""

from datetime import datetime
from extensions import db


class AdminLog(db.Model):
    """Model to track all administrative actions"""
    
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    target_user_id = db.Column(db.Integer, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Admin who performed the action
    admin = db.relationship('User', foreign_keys=[admin_id], backref='admin_actions')
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'admin_name': self.admin.name if self.admin else 'Unknown',
            'action': self.action,
            'details': self.details,
            'target_user_id': self.target_user_id,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }
    
    @classmethod
    def log_action(cls, admin_id: int, action: str, details: str = None,
                   target_user_id: int = None, ip_address: str = None):
        """Convenience method to create and save a log entry"""
        from extensions import db
        log = cls(
            admin_id=admin_id,
            action=action,
            details=details,
            target_user_id=target_user_id,
            ip_address=ip_address
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    def __repr__(self):
        return f'<AdminLog admin={self.admin_id} action={self.action}>'
