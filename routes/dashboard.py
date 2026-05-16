"""
Dashboard Routes
Main user dashboard with disaster support panels
"""

from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from models.chat import ChatHistory
from models.reports import EmergencyReport
from ai_engine.response_engine import get_response_engine

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Main user dashboard"""
    engine = get_response_engine()
    
    # Get user stats
    total_chats = ChatHistory.query.filter_by(user_id=current_user.id).count()
    recent_chats = ChatHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ChatHistory.timestamp.desc()).limit(5).all()
    
    total_reports = EmergencyReport.query.filter_by(user_id=current_user.id).count()
    open_reports = EmergencyReport.query.filter_by(
        user_id=current_user.id, status='open'
    ).count()
    
    # Disaster types for panel
    disaster_types = [
        {'id': 'flood', 'name': 'Flood', 'icon': '🌊', 'color': '#3b82f6', 'desc': 'Rising water emergency guidance'},
        {'id': 'fire', 'name': 'Fire', 'icon': '🔥', 'color': '#ef4444', 'desc': 'Fire safety and escape routes'},
        {'id': 'earthquake', 'name': 'Earthquake', 'icon': '🏚️', 'color': '#f59e0b', 'desc': 'Seismic emergency response'},
        {'id': 'medical', 'name': 'Medical', 'icon': '🏥', 'color': '#ec4899', 'desc': 'Emergency medical assistance'},
        {'id': 'cyclone', 'name': 'Cyclone', 'icon': '🌀', 'color': '#06b6d4', 'desc': 'Storm preparedness guide'},
        {'id': 'landslide', 'name': 'Landslide', 'icon': '⛰️', 'color': '#8b5cf6', 'desc': 'Landslide evacuation guide'},
    ]
    
    return render_template(
        'dashboard.html',
        total_chats=total_chats,
        recent_chats=recent_chats,
        total_reports=total_reports,
        open_reports=open_reports,
        disaster_types=disaster_types
    )


@dashboard_bp.route('/disaster/<disaster_type>')
@login_required
def disaster_info(disaster_type: str):
    """Detailed disaster information page"""
    engine = get_response_engine()
    info = engine.get_disaster_info(disaster_type)
    
    if not info:
        return redirect(url_for('dashboard.index'))
    
    return render_template('disaster_info.html', disaster=info, dtype=disaster_type)


@dashboard_bp.route('/api/map/hotspots')
@login_required
def map_hotspots():
    """Returns disaster hotspots for map rendering"""
    # Dummy data for Leaflet map (normally pulled from DB based on EmergencyReports)
    reports = EmergencyReport.query.filter_by(status='open').all()
    hotspots = []
    
    # Map cities to dummy coordinates for the demo
    city_coords = {
        'Mumbai': (19.0760, 72.8777),
        'Delhi': (28.7041, 77.1025),
        'Chennai': (13.0827, 80.2707),
        'Gujarat': (22.2587, 71.1924)
    }
    
    for r in reports:
        if r.location in city_coords:
            lat, lng = city_coords[r.location]
            hotspots.append({
                'id': r.id,
                'lat': lat,
                'lng': lng,
                'type': r.disaster_type,
                'severity': r.severity,
                'description': r.description
            })
            
    return jsonify({'hotspots': hotspots})

@dashboard_bp.route('/api/map/resources')
@login_required
def map_resources():
    """Returns nearby resources (shelters, hospitals)"""
    from flask import jsonify
    lat = request.args.get('lat', type=float, default=19.0760)
    lng = request.args.get('lng', type=float, default=72.8777)
    
    # Generate mock resources near the requested coordinates
    resources = [
        {'id': 1, 'lat': lat + 0.01, 'lng': lng + 0.01, 'type': 'hospital', 'name': 'City General Hospital'},
        {'id': 2, 'lat': lat - 0.01, 'lng': lng - 0.02, 'type': 'shelter', 'name': 'Relief Camp A'},
        {'id': 3, 'lat': lat + 0.02, 'lng': lng - 0.01, 'type': 'police', 'name': 'Central Police Station'}
    ]
    return jsonify({'resources': resources})
