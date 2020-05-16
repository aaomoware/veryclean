from flask import redirect, render_template, flash, request, url_for, session, current_app
from shop import db, app, photos, Bcrypt
from .models import Register
import secrets, os

@app.route('/customer/register',  methods=['GET', 'POST'])
def customer_register():
    if request.method == 'GET':
        return render_template('customer/register.html')
    if request.method == 'POST':
        try:
            hash_password = Bcrypt.generate_password_hash(request.form.password)
            register = Register (
                password = hash_password,
                email = request.form.get('email'),
                country = request.form.get('country'),
                lastname = request.form.get('lastname'),
                address1 = request.form.get('address1'),
                address2 = request.form.get('address2'),
                province = request.form.get('province'),
                towncity = request.form.get('towncity'),
                firstname = request.form.get('firstname'),
                companyname = request.form.get('companyname'),
                phonenumber = request.form.get('phonenumber'),
                zippostalcode = request.form.get('zippostalcode'))
            db.session.add(register)
            flash(f'Welcome {request.form.firstname}. Thank you for registering', 'success')
        except Exception as e:
            print(e)
    return render_template('customer/login.html')


@app.route('/customer/login',  methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        return render_template('customer/login.html')
    if request.method == 'POST':
        try:
            pass
        except Exception as e:
            print(e)
