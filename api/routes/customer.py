from flask import Blueprint, render_template, request, redirect, url_for, session
from models.products import Product
from models.baskets import Basket
from models.orders import Order
from models.users import User
from werkzeug.security import generate_password_hash

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customer/dashboard')
def customer_dashboard():
    return render_template('customer_dashboard.html')

@customer_bp.route('/customer/products', methods=['GET'])
def customer_products():
    return redirect(url_for('products.get_products'))

@customer_bp.route('/customer/basket/add', methods=['POST'])
def add_to_basket():
    return redirect(url_for('basket.add_to_basket'))

@customer_bp.route('/customer/basket')
def customer_basket():
    basket = Basket.query.filter_by(user_id=session['user_id']).first()
    if not basket or not basket.items:
        return render_template('customer_basket.html', items=[], message="Your basket is empty")
    
    items = []
    for item in basket.items.split(','):
        product_id, quantity = item.split(':')
        product = Product.query.get(product_id)
        items.append({"product": product, "quantity": quantity})
    
    return render_template('customer_basket.html', items=items)

@customer_bp.route('/customer/orders', methods=['GET'])
def customer_orders():
    return redirect(url_for('orders.view_orders'))

@customer_bp.route('/customer/profile', methods=['GET', 'POST'])
def customer_profile():
    return redirect(url_for('profile.profile'))