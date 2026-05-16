"""
Admin Routes
Admin panel for user management, chat monitoring, and system control
"""

from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.chat import ChatHistory
from models.reports import EmergencyReport
from models.admin_logs import AdminLog

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to restrict access to admin users only"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/admin')
@admin_required
def index():
    """Admin dashboard home"""
    # Summary statistics
    total_users = User.query.filter_by(role='user').count()
    total_chats = ChatHistory.query.count()
    open_reports = EmergencyReport.query.filter_by(status='open').count()
    critical_reports = EmergencyReport.query.filter_by(severity='critical', status='open').count()
    escalated_count = EmergencyReport.query.filter_by(is_escalated=True).count()
    
    # Recent activity
    recent_chats = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(10).all()
    recent_reports = EmergencyReport.query.order_by(EmergencyReport.created_at.desc()).limit(10).all()
    recent_logs = AdminLog.query.order_by(AdminLog.timestamp.desc()).limit(10).all()
    
    # Intent distribution for quick chart
    intent_stats = ChatHistory.get_intent_stats()
    intent_data = {row.intent: row.count for row in intent_stats}
    
    return render_template(
        'admin.html',
        total_users=total_users,
        total_chats=total_chats,
        open_reports=open_reports,
        critical_reports=critical_reports,
        escalated_count=escalated_count,
        recent_chats=recent_chats,
        recent_reports=recent_reports,
        recent_logs=recent_logs,
        intent_data=intent_data
    )


@admin_bp.route('/admin/users')
@admin_required
def users():
    """Manage all users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%'))
        )
    
    users_list = query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=15, error_out=False)
    
    return render_template('admin_users.html', users=users_list, search=search)


@admin_bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
@admin_required
def toggle_user(user_id: int):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'error': 'Cannot modify your own account'}), 400
    
    user.is_active = not user.is_active
    db.session.commit()
    
    action = 'activated' if user.is_active else 'deactivated'
    AdminLog.log_action(
        admin_id=current_user.id,
        action=f'User {action}',
        details=f'User {user.email} {action}',
        target_user_id=user.id,
        ip_address=request.remote_addr
    )
    
    return jsonify({'success': True, 'is_active': user.is_active, 'action': action})


@admin_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id: int):
    """Delete a user account"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    email = user.email
    db.session.delete(user)
    db.session.commit()
    
    AdminLog.log_action(
        admin_id=current_user.id,
        action='User deleted',
        details=f'Deleted user account: {email}',
        ip_address=request.remote_addr
    )
    
    flash(f'User {email} deleted successfully.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/admin/chats')
@admin_required
def chats():
    """View all chat logs"""
    page = request.args.get('page', 1, type=int)
    intent_filter = request.args.get('intent', '')
    severity_filter = request.args.get('severity', '')
    
    query = ChatHistory.query
    if intent_filter:
        query = query.filter_by(intent=intent_filter)
    if severity_filter:
        query = query.filter_by(severity=severity_filter)
    
    chats_list = query.order_by(ChatHistory.timestamp.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    intents = db.session.query(ChatHistory.intent).distinct().all()
    intents = [i[0] for i in intents]
    
    return render_template(
        'admin_chats.html',
        chats=chats_list,
        intents=intents,
        intent_filter=intent_filter,
        severity_filter=severity_filter
    )


@admin_bp.route('/admin/reports')
@admin_required
def reports():
    """Manage emergency reports"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = EmergencyReport.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    reports_list = query.order_by(EmergencyReport.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin_reports.html', reports=reports_list, status_filter=status_filter)


@admin_bp.route('/admin/reports/<int:report_id>/status', methods=['POST'])
@admin_required
def update_report_status(report_id: int):
    """Update emergency report status"""
    report = EmergencyReport.query.get_or_404(report_id)
    new_status = request.json.get('status')
    
    valid_statuses = ['open', 'in_progress', 'resolved', 'closed']
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    report.status = new_status
    db.session.commit()
    
    AdminLog.log_action(
        admin_id=current_user.id,
        action='Report status updated',
        details=f'Report #{report_id} status changed to {new_status}',
        ip_address=request.remote_addr
    )
    
    return jsonify({'success': True, 'status': new_status})


@admin_bp.route('/admin/logs')
@admin_required
def logs():
    """View admin action logs"""
    page = request.args.get('page', 1, type=int)
    logs_list = AdminLog.query.order_by(AdminLog.timestamp.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin_logs.html', logs=logs_list)


@admin_bp.route('/admin/ai-training', methods=['GET'])
@admin_required
def ai_training():
    """AI Model Training interface"""
    from ai_engine.intent_classifier import get_classifier
    classifier = get_classifier()
    
    stats = {
        'is_trained': classifier._is_trained,
        'intents_count': len(classifier.label_encoder.classes_) if classifier._is_trained else 0,
    }
    return render_template('admin_ai_training.html', stats=stats)


@admin_bp.route('/admin/ai-training/retrain', methods=['POST'])
@admin_required
def ai_retrain():
    """Trigger AI model retraining"""
    from ai_engine.intent_classifier import get_classifier
    try:
        classifier = get_classifier()
        classifier.train()
        
        AdminLog.log_action(
            admin_id=current_user.id,
            action='AI Model Retrained',
            details='Manually triggered intent classifier retraining',
            ip_address=request.remote_addr
        )
        return jsonify({'success': True, 'message': 'AI Model successfully retrained!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
