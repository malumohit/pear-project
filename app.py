# app.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from models import db, User, Customer, Device, Repair, Service, Part, RepairService, ServicePart
from config import Config
from datetime import datetime
import secrets

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_customers = Customer.query.count()
    total_devices = Device.query.count()
    pending_repairs = Repair.query.filter_by(status='pending').count()
    completed_repairs = Repair.query.filter_by(status='completed').count()
    
    # Recent repairs
    recent_repairs = Repair.query.order_by(Repair.request_date.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_customers=total_customers,
                         total_devices=total_devices,
                         pending_repairs=pending_repairs,
                         completed_repairs=completed_repairs,
                         recent_repairs=recent_repairs)

@app.route('/customers')
@login_required
def customers():
    all_customers = Customer.query.order_by(Customer.name).all()
    return render_template('customers.html', customers=all_customers)

@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        new_customer = Customer(name=name, address=address, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('add_customer.html')

@app.route('/devices')
@login_required
def devices():
    all_devices = Device.query.order_by(Device.device_type).all()
    return render_template('devices.html', devices=all_devices)

@app.route('/repairs')
@login_required
def repairs():
    all_repairs = Repair.query.order_by(Repair.request_date.desc()).all()
    return render_template('repairs.html', repairs=all_repairs)

@app.route('/repairs/add', methods=['GET', 'POST'])
@login_required
def add_repair():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        device_id = request.form.get('device_id')
        problem_description = request.form.get('problem_description')
        
        # Generate unique reference number
        reference_number = f"REP-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"
        
        new_repair = Repair(
            reference_number=reference_number,
            customer_id=customer_id,
            device_id=device_id,
            problem_description=problem_description
        )
        db.session.add(new_repair)
        db.session.commit()
        
        flash('Repair request created successfully!', 'success')
        return redirect(url_for('repairs'))
    
    customers = Customer.query.all()
    devices = Device.query.all()
    return render_template('add_repair.html', customers=customers, devices=devices)

@app.route('/services')
@login_required
def services():
    all_services = Service.query.all()
    return render_template('services.html', services=all_services)

@app.route('/parts')
@login_required
def parts():
    all_parts = Part.query.all()
    return render_template('parts.html', parts=all_parts)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Initialize database tables
@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command('create-admin')
def create_admin():
    """Create an admin user."""
    admin = User(username='admin', role='admin')
    admin.set_password('admin123')  # Change this password!
    db.session.add(admin)
    db.session.commit()
    print('Admin user created! Username: admin, Password: admin123')

if __name__ == '__main__':
    app.run(debug=True)
