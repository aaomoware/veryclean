from flask import redirect, render_template, flash, request, url_for, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, bcrypt, login_manager
from .models import Register, CustomerOrder
import secrets, os

@app.route('/customer/register',  methods=['GET', 'POST'])
def customer_register():
    if request.method == 'GET':
        return render_template('customer/register.html')
    if request.method == 'POST':
        if Register.query.filter_by(email=request.form['email']).first():
            email=request.form['email'] 
            flash(f'{email} has already been registered. Please login or request a password reset', 'warning')
            return render_template('customer/login.html')
        else:
            hash_password = bcrypt.generate_password_hash(request.form['password'])
            firstname = request.form['firstname']
            register = Register (
                password = hash_password,
                email = request.form['email'],
                country = request.form['country'],
                lastname = request.form['lastname'],
                address1 = request.form['address1'],
                address2 = request.form['address2'],
                province = request.form['province'],
                towncity = request.form['towncity'],
                firstname = request.form['firstname'],
                postcode = request.form['zippostalcode'],
                companyname = request.form['companyname'],
                phonenumber = request.form['phonenumber'])
            db.session.add(register)
            flash(f'Welcome {firstname} Thank you for registering', 'success')
            db.session.commit()
            return render_template('customer/login.html')


@app.route('/customer/login',  methods=['GET', 'POST'])
def customerLogin():
    if request.method == 'GET':
        return render_template('customer/login.html')
    if request.method == 'POST':
        user = Register.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('shop'))
        flash(f'Invalid email or password', 'danger')
        return redirect(url_for('customerLogin'))


@app.route('/customer/logout')
def customerLogout():
    logout_user()
    return redirect(url_for('shop'))


@app.route('/getorder', methods=['POST'])
@login_required
def get_order():
    if request.method == 'GET':
        return redirect(url_for('shop'))
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(
                invoice = invoice,
                customer_id = customer_id,
                orders = session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            return render_template('customer/order_complete.html')
        except Exception as e:
            print(e)
            flash('Something went wrong while getting orders', 'danger')
            return redirect(url_for('get_carts'))