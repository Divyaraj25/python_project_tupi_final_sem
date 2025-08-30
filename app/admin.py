from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Customer, Order, SubscriptionPlan
from app.auth.forms import RegistrationForm
from app.decorators import admin_required

# Create admin blueprint
admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get counts for dashboard
    seller_count = User.query.filter_by(role='seller').count()
    customer_count = Customer.query.count()
    order_count = Order.query.count()
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         title='Admin Dashboard',
                         seller_count=seller_count,
                         customer_count=customer_count,
                         order_count=order_count,
                         recent_orders=recent_orders)

@admin.route('/sellers')
@login_required
@admin_required
def sellers():
    all_sellers = User.query.filter_by(role='seller').all()
    return render_template('admin/sellers.html', title='Sellers', sellers=all_sellers)

@admin.route('/seller/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_seller():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='seller'  # Force role to be seller
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Seller account created for {form.username.data}!', 'success')
        return redirect(url_for('admin.sellers'))
    return render_template('admin/add_seller.html', title='Add Seller', form=form)

@admin.route('/customers')
@login_required
@admin_required
def customers():
    all_customers = db.session.query(
        Customer, User.username
    ).join(User, Customer.seller_id == User.id).all()
    return render_template('admin/customers.html', 
                         title='All Customers', 
                         customers=all_customers)

@admin.route('/orders')
@login_required
@admin_required
def orders():
    all_orders = db.session.query(
        Order, 
        Customer.name.label('customer_name'),
        SubscriptionPlan.name.label('plan_name'),
        User.username.label('seller_username')
    ).join(
        Customer, Order.customer_id == Customer.id
    ).join(
        SubscriptionPlan, Order.plan_id == SubscriptionPlan.id
    ).join(
        User, Order.created_by == User.id
    ).order_by(Order.created_at.desc()).all()
    
    return render_template('admin/orders.html', 
                         title='All Orders', 
                         orders=all_orders)
