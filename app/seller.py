from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Customer, Order, SubscriptionPlan
from app.decorators import seller_required
from datetime import datetime

# Route names for URL generation
CREATE_ORDER_ROUTE = 'seller.create_order'

# Create seller blueprint
seller = Blueprint('seller', __name__)

@seller.route('/dashboard')
@login_required
@seller_required
def dashboard():
    # Get counts for the current seller
    customer_count = Customer.query.filter_by(seller_id=current_user.id).count()
    order_count = Order.query.join(
        Customer, Order.customer_id == Customer.id
    ).filter(
        Customer.seller_id == current_user.id
    ).count()
    
    # Get recent orders for the current seller
    recent_orders = db.session.query(
        Order, Customer.name.label('customer_name'), SubscriptionPlan.name.label('plan_name')
    ).join(
        Customer, Order.customer_id == Customer.id
    ).join(
        SubscriptionPlan, Order.plan_id == SubscriptionPlan.id
    ).filter(
        Customer.seller_id == current_user.id
    ).order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('seller/dashboard.html',
                         title='Seller Dashboard',
                         customer_count=customer_count,
                         order_count=order_count,
                         recent_orders=recent_orders)

@seller.route('/customers')
@login_required
@seller_required
def customers():
    seller_customers = Customer.query.filter_by(seller_id=current_user.id).all()
    return render_template('seller/customers.html', 
                         title='My Customers', 
                         customers=seller_customers)

@seller.route('/customer/add', methods=['GET', 'POST'])
@login_required
@seller_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        # Validate required fields
        if not name or not email:
            flash('Name and email are required fields', 'danger')
            return redirect(url_for('seller.add_customer'))
        
        # Check if email already exists for this seller
        existing_customer = Customer.query.filter_by(
            email=email, 
            seller_id=current_user.id
        ).first()
        
        if existing_customer:
            flash('A customer with this email already exists', 'danger')
            return redirect(url_for('seller.add_customer'))
        
        # Create new customer
        new_customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
            seller_id=current_user.id
        )
        
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('seller.customers'))
    
    return render_template('seller/add_customer.html', title='Add Customer')

@seller.route('/orders')
@login_required
@seller_required
def orders():
    seller_orders = db.session.query(
        Order, 
        Customer.name.label('customer_name'),
        SubscriptionPlan.name.label('plan_name')
    ).join(
        Customer, Order.customer_id == Customer.id
    ).join(
        SubscriptionPlan, Order.plan_id == SubscriptionPlan.id
    ).filter(
        Customer.seller_id == current_user.id
    ).order_by(Order.created_at.desc()).all()
    
    return render_template('seller/orders.html', 
                         title='My Orders', 
                         orders=seller_orders)

@seller.route('/order/create', methods=['GET', 'POST'])
@login_required
@seller_required
def create_order():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        plan_id = request.form.get('plan_id')
        start_date_str = request.form.get('start_date')
        
        # Validate required fields
        if not all([customer_id, plan_id, start_date_str]):
            flash('All fields are required', 'danger')
            return redirect(url_for(CREATE_ORDER_ROUTE))
        
        # Check if customer belongs to the current seller
        customer = Customer.query.filter_by(
            id=customer_id, 
            seller_id=current_user.id
        ).first()
        
        if not customer:
            flash('Invalid customer selected', 'danger')
            return redirect(url_for(CREATE_ORDER_ROUTE))
        
        # Check if plan exists
        plan = SubscriptionPlan.query.get(plan_id)
        if not plan:
            flash('Invalid subscription plan selected', 'danger')
            return redirect(url_for(CREATE_ORDER_ROUTE))
        
        # Parse start date
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(url_for(CREATE_ORDER_ROUTE))
        
        # Create new order
        new_order = Order(
            customer_id=customer_id,
            plan_id=plan_id,
            start_date=start_date,
            created_by=current_user.id,
            status='Active'
        )
        
        # Calculate end date based on plan duration
        new_order.calculate_end_date()
        
        db.session.add(new_order)
        db.session.commit()
        
        flash('Order created successfully!', 'success')
        return redirect(url_for('seller.orders'))
    
    # For GET request, fetch customers and plans
    customers = Customer.query.filter_by(seller_id=current_user.id).all()
    plans = SubscriptionPlan.query.all()
    
    return render_template('seller/create_order.html',
                         title='Create Order',
                         customers=customers,
                         plans=plans)
