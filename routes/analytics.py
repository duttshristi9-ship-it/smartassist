"""
Analytics Routes
Charts and data visualization for disaster management insights
"""

from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from extensions import db
from models.chat import ChatHistory
from models.reports import EmergencyReport
from models.user import User

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics')
@login_required
def index():
    """Analytics dashboard page"""
    return render_template('analytics.html')


@analytics_bp.route('/api/analytics/overview')
@login_required
def overview_data():
    """Overall analytics data for dashboard charts"""
    
    # Intent distribution (last 30 days)
    cutoff = datetime.utcnow() - timedelta(days=30)
    
    intent_stats = db.session.query(
        ChatHistory.intent,
        func.count(ChatHistory.id).label('count')
    ).filter(ChatHistory.timestamp >= cutoff)\
     .group_by(ChatHistory.intent)\
     .order_by(func.count(ChatHistory.id).desc())\
     .all()
    
    # Daily activity (last 14 days)
    daily_stats = []
    for i in range(14, -1, -1):
        day = datetime.utcnow() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59)
        count = ChatHistory.query.filter(
            ChatHistory.timestamp >= day_start,
            ChatHistory.timestamp <= day_end
        ).count()
        daily_stats.append({
            'date': day.strftime('%b %d'),
            'count': count
        })
    
    # Severity distribution
    severity_stats = db.session.query(
        ChatHistory.severity,
        func.count(ChatHistory.id).label('count')
    ).group_by(ChatHistory.severity).all()
    
    # Emergency reports by disaster type
    report_stats = db.session.query(
        EmergencyReport.disaster_type,
        func.count(EmergencyReport.id).label('count')
    ).group_by(EmergencyReport.disaster_type).all()
    
    # Report status distribution
    status_stats = db.session.query(
        EmergencyReport.status,
        func.count(EmergencyReport.id).label('count')
    ).group_by(EmergencyReport.status).all()
    
    # User registration trend (last 30 days)
    user_trend = []
    for i in range(14, -1, -1):
        day = datetime.utcnow() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59)
        count = User.query.filter(
            User.created_at >= day_start,
            User.created_at <= day_end
        ).count()
        user_trend.append({
            'date': day.strftime('%b %d'),
            'count': count
        })
    
    # Summary stats
    total_queries = ChatHistory.query.count()
    total_users = User.query.filter_by(role='user').count()
    total_reports = EmergencyReport.query.count()
    open_reports = EmergencyReport.query.filter_by(status='open').count()
    critical_cases = ChatHistory.query.filter_by(severity='critical').count()
    escalated = EmergencyReport.query.filter_by(is_escalated=True).count()
    
    return jsonify({
        'intent_distribution': {
            'labels': [row.intent.replace('_', ' ').title() for row in intent_stats],
            'data': [row.count for row in intent_stats]
        },
        'daily_activity': {
            'labels': [d['date'] for d in daily_stats],
            'data': [d['count'] for d in daily_stats]
        },
        'severity_distribution': {
            'labels': [row.severity.title() for row in severity_stats],
            'data': [row.count for row in severity_stats]
        },
        'report_by_type': {
            'labels': [row.disaster_type for row in report_stats],
            'data': [row.count for row in report_stats]
        },
        'report_status': {
            'labels': [row.status.replace('_', ' ').title() for row in status_stats],
            'data': [row.count for row in status_stats]
        },
        'user_trend': {
            'labels': [d['date'] for d in user_trend],
            'data': [d['count'] for d in user_trend]
        },
        'summary': {
            'total_queries': total_queries,
            'total_users': total_users,
            'total_reports': total_reports,
            'open_reports': open_reports,
            'critical_cases': critical_cases,
            'escalated': escalated
        }
    })
