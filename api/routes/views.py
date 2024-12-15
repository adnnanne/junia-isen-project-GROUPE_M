from flask import Blueprint, render_template, flash, redirect, request, jsonify
from flask_login import login_required, current_user
from intasend import APIService
from api import db
views = Blueprint('views', __name__)

# Replace with actual keys
API_PUBLISHABLE_KEY = 'YOUR_PUBLISHABLE_KEY'
API_TOKEN = 'YOUR_API_TOKEN'


@views.route('/')
def home():
    from api.models import Product, Cart, Order
    items = Product.query.filter_by(flash_sale=True).all()
    cart = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else []
    return render_template('home.html', items=items, cart=cart)


@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    
    from api.models import Product, Cart, Order
    item_to_add = Product.query.get(item_id)
    if not item_to_add:
        flash('Item does not exist.')
        return redirect(request.referrer)

    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()

    if item_exists:
        item_exists.quantity += 1
        flash(f'Quantity of {item_exists.product.product_name} has been updated.')
    else:
        new_cart_item = Cart(
            quantity=1,
            product_link=item_to_add.id,
            customer_link=current_user.id
        )
        db.session.add(new_cart_item)
        flash(f'{item_to_add.product_name} added to cart.')

    db.session.commit()
    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    from api.models import  Cart
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)
    return render_template('cart.html', cart=cart, amount=amount, total=amount + 200)


@views.route('/pluscart')
@login_required
def plus_cart():
    from api.models import Cart
    
    cart_id = request.args.get('cart_id')
    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    cart_item.quantity += 1
    db.session.commit()

    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)

    data = {
        'quantity': cart_item.quantity,
        'amount': amount,
        'total': amount + 200
    }
    return jsonify(data)


@views.route('/minuscart')
@login_required
def minus_cart():
    from api.models import Cart
    cart_id = request.args.get('cart_id')
    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    cart_item.quantity = max(0, cart_item.quantity - 1)
    db.session.commit()
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)

    data = {
        'quantity': cart_item.quantity,
        'amount': amount,
        'total': amount + 200
    }
    return jsonify(data)


@views.route('/removecart')
@login_required
def remove_cart():
    from api.models import Cart
    # Get the cart item ID from the request arguments
    cart_id = request.args.get('cart_id')
    if not cart_id:
        flash('Cart item ID is missing!')
        return redirect('/cart')

    try:
        # Fetch the cart item by ID
        cart_item = Cart.query.get(cart_id)

        # If the cart item doesn't exist, notify the user
        if not cart_item:
            flash('Cart item not found.')
            return redirect('/cart')

        # Remove the item from the cart and commit the transaction
        db.session.delete(cart_item)
        db.session.commit()

        # Recalculate the total and amount for the cart
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        data = {
            'amount': amount,
            'total': amount + 200  # Assuming 200 is a fixed shipping fee or other costs
        }

        # Optionally, return a JSON response or redirect to the cart page
        flash('Item removed from cart.')
        return redirect('/cart')

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error removing item from cart: {e}")
        flash('An error occurred while removing the item from the cart.')
        return redirect('/cart')


@views.route('/place-order')
@login_required
def place_order():
    
    from api.models import Product, Cart, Order
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if not customer_cart:
        flash('Your cart is empty.')
        return redirect('/')

    try:
        total = sum(item.product.current_price * item.quantity for item in customer_cart)

        service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
        create_order_response = service.collect.mpesa_stk_push(
            phone_number='YOUR_NUMBER',
            email=current_user.email,
            amount=total + 200,
            narrative='Purchase of goods'
        )

        for item in customer_cart:
            new_order = Order(
                quantity=item.quantity,
                price=item.product.current_price,
                status=create_order_response['invoice']['state'].capitalize(),
                payment_id=create_order_response['id'],
                product_link=item.product_link,
                customer_link=current_user.id
            )
            db.session.add(new_order)

            product = Product.query.get(item.product_link)
            product.in_stock -= item.quantity

            db.session.delete(item)

        db.session.commit()
        flash('Order placed successfully.')
        return redirect('/orders')
    except Exception as e:
        print('Error placing order:', e)
        flash('Order could not be placed.')
        return redirect('/')


@views.route('/orders')
@login_required
def order():
    from api.models import  Order
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)


@views.route('/search', methods=['GET', 'POST'])
def search():
    from api.models import Product, Cart
    if request.method == 'POST':
        search_query = request.form.get('search', '')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        cart = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else []
        return render_template('search.html', items=items, cart=cart)

    return render_template('search.html')
