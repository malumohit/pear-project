# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    repairs = db.relationship('Repair', backref='customer', lazy=True)

class Device(db.Model):
    __tablename__ = 'devices'
    device_id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(50), nullable=False)  # smartphone, laptop, tablet, MP3
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    repairs = db.relationship('Repair', backref='device', lazy=True)

class Repair(db.Model):
    __tablename__ = 'repairs'
    repair_id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.device_id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    problem_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    completion_date = db.Column(db.DateTime)
    
    # Relationships
    repair_services = db.relationship('RepairService', backref='repair', lazy=True)

class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    charge = db.Column(db.Numeric(10, 2), nullable=False)  # Changed from Decimal to Numeric
    
    # Relationships
    repair_services = db.relationship('RepairService', backref='service', lazy=True)
    service_parts = db.relationship('ServicePart', backref='service', lazy=True)

class Part(db.Model):
    __tablename__ = 'parts'
    part_id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity_in_stock = db.Column(db.Integer, default=0)
    cost = db.Column(db.Numeric(10, 2), nullable=False)  # Changed from Decimal to Numeric
    
    # Relationships
    service_parts = db.relationship('ServicePart', backref='part', lazy=True)

# Junction Tables
class RepairService(db.Model):
    __tablename__ = 'repair_services'
    id = db.Column(db.Integer, primary_key=True)
    repair_id = db.Column(db.Integer, db.ForeignKey('repairs.repair_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
    date_performed = db.Column(db.DateTime, default=datetime.utcnow)

class ServicePart(db.Model):
    __tablename__ = 'service_parts'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.part_id'), nullable=False)
    quantity_required = db.Column(db.Integer, nullable=False, default=1)
