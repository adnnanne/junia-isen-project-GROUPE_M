from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from models.products import Product
from models.orders import Order
from models.users import User
from forms import ShopItemsForm, OrderForm  # Add Flask-WTF forms for validation
from . import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.id != 1:  # Admin check
        return render_template('404.html')
    return render_template('admin_dashboard.html')

@admin_bp.route('/admin/products', methods=['GET', 'POST'])
@login_required
def manage_products():
    if current_user.id != 1:  # Admin check
        return render_template('404.html')

    form = ShopItemsForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            product_name = form.product_name.data
            current_price = form.current_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_product = Product(
                name=product_name, price=current_price,
                stock=in_stock, flash_sale=flash_sale,
                product_picture=file_path
            )

            db.session.add(new_product)
            db.session.commit()
            flash(f"{product_name} added successfully!", "success")
        except Exception as e:
            flash(f"Error adding product: {str(e)}", "danger")

    products = Product.query.all()
    return render_template('admin_products.html', form=form, products=products)

@admin_bp.route('/admin/orders', methods=['GET', 'POST'])
@login_required
def get_all_orders():
    if current_user.id != 1:
        return render_template('404.html')

    orders = Order.query.order_by(Order.date_created).all()
    return render_template('admin_orders.html', orders=orders)

@admin_bp.route('/admin/orders/update/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id != 1:
        return render_template('404.html')

    form = OrderForm()
    order = Order.query.get_or_404(order_id)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            order.status = form.order_status.data
            db.session.commit()
            flash(f"Order {order.id} updated successfully!", "success")
            return redirect(url_for('admin.get_all_orders'))
        except Exception as e:
            flash(f"Error updating order: {str(e)}", "danger")

    return render_template('update_order.html', form=form, order=order)

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.id != 1:
        return render_template('404.html')

    if request.method == 'POST':
        data = request.form
        try:
            hashed_password = generate_password_hash(data['password'], method='sha256')
            user = User(username=data['username'], password=hashed_password, role=data['role'])
            db.session.add(user)
            db.session.commit()
            flash("User added successfully!", "success")
        except Exception as e:
            flash(f"Error adding user: {str(e)}", "danger")

    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.id != 1:
        return render_template('404.html')

    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "danger")

    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/admin/customers')
@login_required
def display_customers():
    if current_user.id != 1:
        return render_template('404.html')

    customers = User.query.all()
    return render_template('admin_customers.html', customers=customers)

@admin_bp.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    if current_user.id != 1:
        return render_template('404.html')

    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        data = request.form
        try:
            if data.get('username'):
                user.username = data['username']
            if data.get('password'):
                user.password = generate_password_hash(data['password'], method='sha256')
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating profile: {str(e)}", "danger")

    return render_template('admin_profile.html', user=user)
