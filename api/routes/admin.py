from flask import Blueprint, request, jsonify, render_template
from models.products import Product
from models.orders import Order
from models.users import User
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/admin/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        data = request.form
        product = Product(name=data['name'], price=data['price'], stock=data['stock'], category=data['category'])
        product.save()
        return jsonify({"message": "Product added successfully"}), 201
    return render_template('admin_products.html')

@admin_bp.route('/admin/orders', methods=['GET'])
def get_all_orders():
    user_id = request.args.get('user_id')
    if user_id:
        orders = Order.query.filter_by(user_id=user_id).all()
    else:
        orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        data = request.form
        hashed_password = generate_password_hash(data['password'], method='sha256')
        user = User(username=data['username'], password=hashed_password, role=data['role'])
        user.save()
        return jsonify({"message": "User added successfully"}), 201
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200