from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app import db, bcrypt
from app.models import User, Customer, Order, SubscriptionPlan
from . import bp
from app.decorators import admin_required
from app.auth.forms import RegistrationForm

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get counts for the admin dashboard
    total_sellers = User.query.filter_by(role='seller').count()
    total_customers = Customer.query.count()
    total_orders = Order.query.count()
    
    # Get recent orders with related data
    recent_orders_query = db.session.query(
        Order,
        Customer.name.label('customer_name'),
        User.username.label('seller_username'),
        SubscriptionPlan.name.label('plan_name')
    )
    recent_orders_query = recent_orders_query.join(Customer, Order.customer_id == Customer.id)
    recent_orders_query = recent_orders_query.join(User, Customer.seller_id == User.id)
    recent_orders_query = recent_orders_query.join(SubscriptionPlan, Order.plan_id == SubscriptionPlan.id)
    recent_orders_result = recent_orders_query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Convert Row objects to dictionaries for easier template access
    recent_orders = [{
        'order': order[0],
        'customer_name': order[1],
        'seller_username': order[2],
        'plan_name': order[3]
    } for order in recent_orders_result]
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_sellers=total_sellers,
                         total_customers=total_customers,
                         total_orders=total_orders,
                         recent_orders=recent_orders)

@bp.route('/sellers')
@login_required
@admin_required
def sellers():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of sellers per page
    
    # Get paginated sellers
    pagination = User.query.filter_by(role='seller').order_by(User.username).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/sellers.html', 
                         title='Manage Sellers',
                         sellers=pagination.items,
                         pagination=pagination)

@bp.route('/sellers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_seller():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role='seller',
            is_approved=True
        )
        db.session.add(user)
        db.session.commit()
        flash(f'New seller account created for {form.username.data}!', 'success')
        return redirect(url_for('admin.sellers'))
    return render_template('admin/add_seller.html', 
                         title='Add New Seller',
                         form=form,
                         legend='Add New Seller')

@bp.route('/customers')
@login_required
@admin_required
def customers():
    all_customers = db.session.query(
        Customer, 
        User.username.label('seller_username')
    ).join(
        User, Customer.seller_id == User.id
    ).all()
    return render_template('admin/customers.html', 
                         title='All Customers', 
                         customers=all_customers)

@bp.route('/orders')
@login_required
@admin_required
def orders():
    # Query orders with related data
    query = db.session.query(
        Order,
        Customer.name.label('customer_name'),
        User.username.label('seller_username'),
        SubscriptionPlan.name.label('plan_name')
    )
    query = query.join(Customer, Order.customer_id == Customer.id)
    query = query.join(User, Customer.seller_id == User.id)
    query = query.join(SubscriptionPlan, Order.plan_id == SubscriptionPlan.id)
    all_orders = query.order_by(Order.created_at.desc()).all()
    
    # Convert Row objects to dictionaries for easier template access
    orders_data = [{
        'order': order[0],
        'customer_name': order[1],
        'seller_username': order[2],
        'plan_name': order[3]
    } for order in all_orders]
    
    # Get all sellers for the filter dropdown
    all_sellers = User.query.filter_by(role='seller').all()
    
    return render_template('admin/orders.html',
                         title='Manage Orders',
                         orders=orders_data,
                         all_sellers=all_sellers)
