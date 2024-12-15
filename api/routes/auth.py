from flask import Blueprint, render_template, flash, redirect, url_for
from api.models.forms import LoginForm, SignUpForm, PasswordChangeForm
from api.models import Customer
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from api import db

auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = generate_password_hash(password2)

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully, You can now Login', "success")
                return redirect(url_for('auth.login'))
            except Exception as e:
                print(e)
                flash('Account Not Created! Email already exists.', "danger")

        form.email.data = ''
        form.username.data = ''
        form.password1.data = ''
        form.password2.data = ''

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer and customer.verify_password(password):
            login_user(customer)
            return redirect('/')
        else:
            flash('Incorrect Email or Password', "danger")

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')


@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    if customer_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.profile', customer_id=current_user.id))

    return render_template('profile.html', customer=current_user)


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    if customer_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.profile', customer_id=current_user.id))

    form = PasswordChangeForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if check_password_hash(current_user.password, current_password):
            if new_password == confirm_new_password:
                current_user.password = generate_password_hash(new_password)
                db.session.commit()
                flash("Password updated successfully.", "success")
                return redirect(url_for('auth.profile', customer_id=current_user.id))
            else:
                flash("New passwords do not match.", "danger")
        else:
            flash("Current password is incorrect.", "danger")

    return render_template('change_password.html', form=form)