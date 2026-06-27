"""
EmergencyReport Model
Tracks reported emergencies from users
"""

from datetime import datetime
from extensions import db


class EmergencyReport(db.Model):
    """Model for tracking emergency reports submitted by users"""
    
    __tablename__ = 'emergency_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    disaster_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='open')  # open, in_progress, resolved, closed
    is_escalated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Severity color mapping for UI
    SEVERITY_COLORS = {
        'low': '#22c55e',
        'medium': '#f59e0b',
        'high': '#ef4444',
        'critical': '#dc2626'
    }
    
    # Status badge mapping
    STATUS_BADGES = {
        'open': 'badge-danger',
        'in_progress': 'badge-warning',
        'resolved': 'badge-success',
        'closed': 'badge-secondary'
    }
    
    def to_dict(self) -> dict:
        """Serialize emergency report"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'disaster_type': self.disaster_type,
            'location': self.location or 'Unknown',
            'severity': self.severity,
            'description': self.description,
            'status': self.status,
            'is_escalated': self.is_escalated,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }
    
    @property
    def severity_color(self) -> str:
        return self.SEVERITY_COLORS.get(self.severity, '#6b7280')
    
    @property
    def status_badge(self) -> str:
        return self.STATUS_BADGES.get(self.status, 'badge-secondary')
    
    def __repr__(self):
        return f'<EmergencyReport {self.disaster_type} [{self.severity}]>'
