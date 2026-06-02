from flask import Flask, render_template, request, jsonify
from database import db, Equipment, MaintenanceSchedule, ServiceHistory
from datetime import datetime, timedelta

# Create Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables when app starts
with app.app_context():
    db.create_all()


# ============ PAGE ROUTES ============

@app.route('/')
def dashboard():
    """Home page - Dashboard"""
    return render_template('dashboard.html')


@app.route('/equipment')
def equipment_page():
    """Equipment management page"""
    return render_template('equipment.html')


@app.route('/maintenance')
def maintenance_page():
    """Maintenance schedule page"""
    return render_template('maintenance.html')


@app.route('/service-history')
def service_history_page():
    """Service history page"""
    return render_template('service_history.html')


# ============ EQUIPMENT API ============

@app.route('/api/equipment', methods=['GET'])
def get_all_equipment():
    """Get all equipment"""
    equipment = Equipment.query.all()
    return jsonify({
        'success': True,
        'data': [e.to_dict() for e in equipment]
    })


@app.route('/api/equipment/<int:id>', methods=['GET'])
def get_equipment(id):
    """Get single equipment"""
    equipment = Equipment.query.get_or_404(id)
    return jsonify({
        'success': True,
        'data': equipment.to_dict()
    })


@app.route('/api/equipment', methods=['POST'])
def create_equipment():
    """Create new equipment"""
    data = request.get_json()
    
    # Check if equipment already exists
    if Equipment.query.filter_by(name=data.get('name')).first():
        return jsonify({'success': False, 'error': 'Equipment already exists'}), 400
    
    equipment = Equipment(
        name=data.get('name'),
        equipment_type=data.get('equipment_type'),
        location=data.get('location'),
        serial_number=data.get('serial_number'),
        manufacturer=data.get('manufacturer'),
        status=data.get('status', 'active')
    )
    
    db.session.add(equipment)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': equipment.to_dict(),
        'message': 'Equipment created successfully'
    }), 201


@app.route('/api/equipment/<int:id>', methods=['PUT'])
def update_equipment(id):
    """Update equipment"""
    equipment = Equipment.query.get_or_404(id)
    data = request.get_json()
    
    equipment.name = data.get('name', equipment.name)
    equipment.equipment_type = data.get('equipment_type', equipment.equipment_type)
    equipment.location = data.get('location', equipment.location)
    equipment.serial_number = data.get('serial_number', equipment.serial_number)
    equipment.manufacturer = data.get('manufacturer', equipment.manufacturer)
    equipment.status = data.get('status', equipment.status)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': equipment.to_dict(),
        'message': 'Equipment updated successfully'
    })


@app.route('/api/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    """Delete equipment"""
    equipment = Equipment.query.get_or_404(id)
    db.session.delete(equipment)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Equipment deleted successfully'
    })


# ============ MAINTENANCE API ============

@app.route('/api/maintenance', methods=['GET'])
def get_all_maintenance():
    """Get all maintenance schedules"""
    maintenance = MaintenanceSchedule.query.all()
    return jsonify({
        'success': True,
        'data': [m.to_dict() for m in maintenance]
    })


@app.route('/api/maintenance', methods=['POST'])
def create_maintenance():
    """Create new maintenance schedule"""
    data = request.get_json()
    
    # Calculate next due date
    next_due = datetime.now().date() + timedelta(days=data.get('frequency_days', 30))
    
    maintenance = MaintenanceSchedule(
        equipment_id=data.get('equipment_id'),
        task_name=data.get('task_name'),
        frequency_days=data.get('frequency_days'),
        next_due_date=next_due,
        priority=data.get('priority', 'medium')
    )
    
    db.session.add(maintenance)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': maintenance.to_dict(),
        'message': 'Maintenance schedule created successfully'
    }), 201


@app.route('/api/maintenance/<int:id>', methods=['PUT'])
def update_maintenance(id):
    """Update maintenance schedule"""
    maintenance = MaintenanceSchedule.query.get_or_404(id)
    data = request.get_json()
    
    maintenance.task_name = data.get('task_name', maintenance.task_name)
    maintenance.frequency_days = data.get('frequency_days', maintenance.frequency_days)
    maintenance.priority = data.get('priority', maintenance.priority)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': maintenance.to_dict(),
        'message': 'Maintenance updated successfully'
    })


@app.route('/api/maintenance/<int:id>', methods=['DELETE'])
def delete_maintenance(id):
    """Delete maintenance schedule"""
    maintenance = MaintenanceSchedule.query.get_or_404(id)
    db.session.delete(maintenance)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Maintenance deleted successfully'
    })


@app.route('/api/maintenance/<int:id>/complete', methods=['POST'])
def complete_maintenance(id):
    """Mark maintenance as completed"""
    maintenance = MaintenanceSchedule.query.get_or_404(id)
    data = request.get_json()
    
    # Update maintenance
    today = datetime.now().date()
    maintenance.last_completed_date = today
    maintenance.next_due_date = today + timedelta(days=maintenance.frequency_days)
    
    # Create service history record
    service = ServiceHistory(
        equipment_id=maintenance.equipment_id,
        maintenance_id=id,
        service_date=today,
        technician_name=data.get('technician_name', 'Unknown'),
        description=data.get('description'),
        duration_hours=data.get('duration_hours'),
        cost=data.get('cost', 0)
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Maintenance marked as completed',
        'data': maintenance.to_dict()
    })


# ============ SERVICE HISTORY API ============

@app.route('/api/service-history', methods=['GET'])
def get_service_history():
    """Get all service history"""
    history = ServiceHistory.query.order_by(ServiceHistory.service_date.desc()).all()
    return jsonify({
        'success': True,
        'data': [h.to_dict() for h in history]
    })


@app.route('/api/service-history', methods=['POST'])
def create_service_history():
    """Create new service record"""
    data = request.get_json()
    
    service = ServiceHistory(
        equipment_id=data.get('equipment_id'),
        maintenance_id=data.get('maintenance_id'),
        service_date=datetime.strptime(data.get('service_date'), '%Y-%m-%d').date(),
        technician_name=data.get('technician_name'),
        description=data.get('description'),
        duration_hours=data.get('duration_hours'),
        cost=data.get('cost', 0)
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': service.to_dict(),
        'message': 'Service record created successfully'
    }), 201


# ============ ANALYTICS API ============

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get dashboard statistics"""
    total_equipment = Equipment.query.count()
    total_schedules = MaintenanceSchedule.query.count()
    total_services = ServiceHistory.query.count()
    
    # Count overdue maintenance
    today = datetime.now().date()
    overdue = MaintenanceSchedule.query.filter(MaintenanceSchedule.next_due_date < today).count()
    
    # Total cost
    total_cost = db.session.query(db.func.sum(ServiceHistory.cost)).scalar() or 0
    
    # Recent services
    recent_services = ServiceHistory.query.order_by(ServiceHistory.service_date.desc()).limit(5).all()
    
    return jsonify({
        'success': True,
        'data': {
            'total_equipment': total_equipment,
            'total_schedules': total_schedules,
            'total_services': total_services,
            'overdue_maintenance': overdue,
            'total_cost': round(total_cost, 2),
            'recent_services': [s.to_dict() for s in recent_services]
        }
    })


# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': 'Server error'}), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)