# test_admin_routes.py
import os
import tempfile
import pytest
from app import create_app, db
from flask_login import login_user
from models import User, Product, Order, Customer
from io import BytesIO

@pytest.fixture
def client():
    app = create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add a test admin user
            admin_user = User(username="admin", email="admin@test.com", role="admin")
            admin_user.set_password("password")
            db.session.add(admin_user)
            db.session.commit()
        yield client
    os.close(db_fd)

# Test for /media/<path:filename>
def test_get_image(client):
    # Simulate a file in the media directory
    media_path = os.path.join(tempfile.gettempdir(), "test.jpg")
    with open(media_path, "wb") as f:
        f.write(b"test image data")

    # Override app config to point to media directory
    with client.application.app_context():
        client.application.config["MEDIA_FOLDER"] = tempfile.gettempdir()

    response = client.get(f'/media/{os.path.basename(media_path)}')
    assert response.status_code == 200
    assert b"test image data" in response.data

# Test for /add-shop-items route
def test_add_shop_items(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)
    
    # POST request to add a product
    response = client.post('/add-shop-items', data={
        'product_name': 'Test Product',
        'current_price': 10.99,
        'previous_price': 12.99,
        'in_stock': 100,
        'flash_sale': True,
        'product_picture': (BytesIO(b"test data"), "test.jpg")
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'added Successfully' in response.data

# Test for /shop-items route
def test_shop_items(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)

    # Add a product to the database
    product = Product(name='Sample Product', price=20.0, stock=5, description='Test product')
    db.session.add(product)
    db.session.commit()

    # GET request to shop-items route
    response = client.get('/shop-items')
    assert response.status_code == 200
    assert b'Sample Product' in response.data

# Test for /update-item/<int:item_id> route
def test_update_item(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)

    # Add a product to update
    product = Product(name='Old Product', price=20.00, stock=10)
    db.session.add(product)
    db.session.commit()

    # Update the product
    response = client.post(f'/update-item/{product.id}', data={
        'product_name': 'Updated Product',
        'current_price': 25.00,
        'previous_price': 20.00,
        'in_stock': 15,
        'flash_sale': False,
        'product_picture': (BytesIO(b"updated data"), "updated.jpg")
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'updated Successfully' in response.data

# Test for /delete-item/<int:item_id> route
def test_delete_item(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)

    # Add a product to delete
    product = Product(name='Product to Delete', price=15.00, stock=5)
    db.session.add(product)
    db.session.commit()

    # Delete the product
    response = client.get(f'/delete-item/{product.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'One Item deleted' in response.data

# Test for /view-orders route
def test_view_orders(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)

    # Add an order to the database
    order = Order(user_id=admin_user.id, total_price=50.00, status='Pending')
    db.session.add(order)
    db.session.commit()

    # GET request to view-orders route
    response = client.get('/view-orders')
    assert response.status_code == 200
    assert b'Pending' in response.data

# Test for /update-order/<int:order_id> route
def test_update_order(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)

    # Add an order to update
    order = Order(user_id=admin_user.id, total_price=50.00, status='Pending')
    db.session.add(order)
    db.session.commit()

    # Update the order
    response = client.post(f'/update-order/{order.id}', data={
        'order_status': 'Completed'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Order Updated successfully' in response.data

# Test for /customers route
def test_display_customers(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)

    # Add a customer to the database
    customer = Customer(username='Test Customer', email='test@customer.com')
    db.session.add(customer)
    db.session.commit()

    # GET request to customers route
    response = client.get('/customers')
    assert response.status_code == 200
    assert b'Test Customer' in response.data

# Test for /admin-page route
def test_admin_page(client):
    # Login as admin
    with client.session_transaction() as sess:
        admin_user = User.query.filter_by(username="admin").first()
        login_user(admin_user)

    response = client.get('/admin-page')
    assert response.status_code == 200
    assert b'Admin Page' in response.data

