"""
Chat Routes
Handles AI chatbot interface and API endpoints
"""

import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from extensions import db
from models.chat import ChatHistory
from models.reports import EmergencyReport
from ai_engine.response_engine import get_response_engine

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chatbot')
@login_required
def chatbot():
    """AI Chatbot interface"""
    # Get or create session ID
    if 'chat_session_id' not in session:
        session['chat_session_id'] = str(uuid.uuid4())
    
    # Fetch recent chat history for this user
    history = ChatHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ChatHistory.timestamp.desc())\
        .limit(50).all()
    history.reverse()  # Chronological order
    
    return render_template('chatbot.html', history=history)


@chat_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    REST API endpoint for chat messages.
    POST /api/chat
    Body: {"message": "user message text"}
    Returns: JSON with AI response and metadata
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        if len(user_message) > 1000:
            return jsonify({'error': 'Message too long (max 1000 characters)'}), 400
        
        # Generate AI response
        engine = get_response_engine()
        result = engine.generate_response(user_message)
        
        # Save to database
        chat_entry = ChatHistory(
            user_id=current_user.id,
            user_message=user_message,
            bot_response=result['response'],
            intent=result['intent'],
            confidence=result['confidence'],
            severity=result['severity'],
            session_id=session.get('chat_session_id'),
            template_idx=result.get('template_idx', 0)
        )
        db.session.add(chat_entry)
        
        # Auto-create emergency report for critical cases
        if result['needs_escalation'] and result['severity'] in ['critical', 'high']:
            report = EmergencyReport(
                user_id=current_user.id,
                disaster_type=result['disaster_type'],
                location=result.get('location'),
                severity=result['severity'],
                description=user_message,
                status='open',
                is_escalated=True
            )
            db.session.add(report)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': result['response'],
            'follow_up': result.get('follow_up', ''),
            'intent': result['intent'],
            'confidence': result['confidence'],
            'severity': result['severity'],
            'needs_escalation': result['needs_escalation'],
            'disaster_type': result['disaster_type'],
            'icon': result['icon'],
            'timestamp': datetime.utcnow().strftime('%H:%M'),
            'chat_id': chat_entry.id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal error: {str(e)}'}), 500


@chat_bp.route('/api/chat/feedback', methods=['POST'])
@login_required
def chat_feedback():
    """Receive feedback for ML training"""
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        rating = data.get('rating') # Expected 0.0 to 1.0
        
        if chat_id is None or rating is None:
            return jsonify({'error': 'Missing parameters'}), 400
            
        chat_entry = ChatHistory.query.get(chat_id)
        if not chat_entry or chat_entry.user_id != current_user.id:
            return jsonify({'error': 'Not found'}), 404
            
        chat_entry.feedback_rating = float(rating)
        db.session.commit()
        
        # Train ML Feedback loop
        engine = get_response_engine()
        engine.submit_feedback(
            message=chat_entry.user_message,
            intent=chat_entry.intent,
            template_idx=chat_entry.template_idx,
            rating=float(rating)
        )
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==========================================
# WebSocket Events for Real-time Comms
# ==========================================

from flask_socketio import emit, join_room, leave_room
from extensions import socketio

@socketio.on('join')
def on_join(data):
    if current_user.is_authenticated:
        room = f"user_{current_user.id}"
        join_room(room)
        # Also join an admin room if they are an admin
        if current_user.role == 'admin':
            join_room('admin_alerts')

@socketio.on('typing')
def on_typing(data):
    if current_user.is_authenticated and current_user.role == 'admin':
        # Admin is typing to a specific user
        user_id = data.get('user_id')
        if user_id:
            emit('admin_typing', {'status': True}, room=f"user_{user_id}")

@socketio.on('admin_message')
def on_admin_message(data):
    if current_user.is_authenticated and current_user.role == 'admin':
        user_id = data.get('user_id')
        message = data.get('message')
        if user_id and message:
            # Emit directly to the user's room
            emit('new_message', {
                'message': message,
                'sender': 'Admin',
                'timestamp': datetime.utcnow().strftime('%H:%M')
            }, room=f"user_{user_id}")
            
            # Save the admin message to ChatHistory
            try:
                chat_entry = ChatHistory(
                    user_id=user_id,
                    user_message='[Admin takeover]',
                    bot_response=message,
                    intent='admin_override',
                    confidence=1.0,
                    severity='high'
                )
                db.session.add(chat_entry)
                db.session.commit()
            except Exception as e:
                db.session.rollback()


@chat_bp.route('/api/chat/history', methods=['GET'])
@login_required
def chat_history():
    """Get user's chat history as JSON"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    history = ChatHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ChatHistory.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'messages': [msg.to_dict() for msg in history.items],
        'total': history.total,
        'pages': history.pages,
        'current_page': page
    })


@chat_bp.route('/api/chat/clear', methods=['POST'])
@login_required
def clear_history():
    """Clear user's chat history"""
    ChatHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Chat history cleared'})


@chat_bp.route('/api/report-emergency', methods=['POST'])
@login_required
def report_emergency():
    """Submit an emergency report"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    report = EmergencyReport(
        user_id=current_user.id,
        disaster_type=data.get('disaster_type', 'Unknown'),
        location=data.get('location', ''),
        severity=data.get('severity', 'medium'),
        description=data.get('description', ''),
        status='open',
        is_escalated=data.get('severity') in ['high', 'critical']
    )
    db.session.add(report)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Emergency report submitted successfully',
        'report_id': report.id
    })
