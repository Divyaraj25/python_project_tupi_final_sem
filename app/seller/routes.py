from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Customer, Order, SubscriptionPlan
from . import bp
from app.decorators import seller_required

@bp.route('/dashboard')
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

@bp.route('/customers')
@login_required
@seller_required
def customers():
    seller_customers = Customer.query.filter_by(seller_id=current_user.id).all()
    return render_template('seller/customers.html', 
                         title='My Customers', 
                         customers=seller_customers)

@bp.route('/orders')
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

@bp.route('/customer/add', methods=['GET', 'POST'])
@login_required
@seller_required
def add_customer():
    from app.forms import CustomerForm
    
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            seller_id=current_user.id
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('seller.customers'))
    
    return render_template('seller/add_customer.html',
                         title='Add Customer',
                         form=form)

@bp.route('/order/create', methods=['GET', 'POST'])
@login_required
@seller_required
def create_order():
    from app.forms import OrderForm
    
    form = OrderForm()
    # Filter customers to only show those belonging to the current seller
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.filter_by(seller_id=current_user.id).all()]
    
    if form.validate_on_submit():
        order = Order(
            customer_id=form.customer_id.data,
            plan_id=form.plan_id.data,
            start_date=form.start_date.data,
            status='Active',
            created_by=current_user.id
        )
        order.calculate_end_date()
        db.session.add(order)
        db.session.commit()
        flash('Order created successfully!', 'success')
        return redirect(url_for('seller.orders'))
    
    return render_template('seller/create_order.html',
                         title='Create Order',
                         form=form)
