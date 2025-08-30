from app import create_app, db
from app.models import User, Customer, SubscriptionPlan, Order
from datetime import datetime, timedelta, timezone

def init_db():
    app = create_app()
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create a test seller
        seller = User(
            username='testseller',
            email='seller@example.com',
            role='seller'
        )
        seller.set_password('seller123')
        
        # Only add seller if not exists
        if not User.query.filter_by(username='testseller').first():
            db.session.add(seller)
            db.session.commit()
            
            # Create test data only if we just created the seller
            create_test_data(seller)
        
        print("Database initialized successfully!")
        print("Admin credentials:")
        print(f"Username: admin")
        print(f"Password: admin123")
        print("\nTest seller credentials:")
        print(f"Username: testseller")
        print(f"Password: seller123")

def create_test_data(seller):
    """Create test data for the application"""
    # Create subscription plans
    plans = [
        SubscriptionPlan(
            name='Basic',
            description='Basic subscription plan',
            price=29.99,
            duration_days=30
        ),
        SubscriptionPlan(
            name='Premium',
            description='Premium subscription plan with all features',
            price=49.99,
            duration_days=30
        )
    ]
    db.session.add_all(plans)
    
    # Create test customers
    customers = [
        Customer(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Main St, City',
            seller_id=seller.id
        ),
        Customer(
            name='Jane Smith',
            email='jane@example.com',
            phone='0987654321',
            address='456 Oak Ave, Town',
            seller_id=seller.id
        )
    ]
    db.session.add_all(customers)
    db.session.commit()
    
    # Create test orders
    now = datetime.now(timezone.utc)
    orders = [
        Order(
            customer_id=customers[0].id,
            plan_id=plans[0].id,
            start_date=now,
            end_date=now + timedelta(days=30),
            status='Active',
            created_by=seller.id
        ),
        Order(
            customer_id=customers[1].id,
            plan_id=plans[1].id,
            start_date=now - timedelta(days=15),
            end_date=now + timedelta(days=15),
            status='Active',
            created_by=seller.id
        )
    ]
    db.session.add_all(orders)
    db.session.commit()

if __name__ == '__main__':
    init_db()
