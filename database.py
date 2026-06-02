from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============ EQUIPMENT TABLE ============
class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    equipment_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to maintenance schedules
    maintenance_schedules = db.relationship('MaintenanceSchedule', backref='equipment', cascade='all, delete-orphan')
    service_history = db.relationship('ServiceHistory', backref='equipment', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipment_type': self.equipment_type,
            'location': self.location,
            'serial_number': self.serial_number,
            'manufacturer': self.manufacturer,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else None
        }


# ============ MAINTENANCE SCHEDULE TABLE ============
class MaintenanceSchedule(db.Model):
    __tablename__ = 'maintenance_schedule'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    task_name = db.Column(db.String(200), nullable=False)
    frequency_days = db.Column(db.Integer, nullable=False)
    last_completed_date = db.Column(db.Date)
    next_due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    service_history = db.relationship('ServiceHistory', backref='maintenance', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'task_name': self.task_name,
            'frequency_days': self.frequency_days,
            'last_completed_date': self.last_completed_date.strftime('%Y-%m-%d') if self.last_completed_date else None,
            'next_due_date': self.next_due_date.strftime('%Y-%m-%d') if self.next_due_date else None,
            'priority': self.priority,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else None
        }


# ============ SERVICE HISTORY TABLE ============
class ServiceHistory(db.Model):
    __tablename__ = 'service_history'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance_schedule.id'))
    service_date = db.Column(db.Date, nullable=False)
    technician_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration_hours = db.Column(db.Float)
    cost = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'maintenance_id': self.maintenance_id,
            'service_date': self.service_date.strftime('%Y-%m-%d') if self.service_date else None,
            'technician_name': self.technician_name,
            'description': self.description,
            'duration_hours': self.duration_hours,
            'cost': self.cost,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else None
        }