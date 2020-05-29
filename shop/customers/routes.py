from flask import redirect, render_template, flash, request, url_for, session, current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, bcrypt, login_manager, cal_cart_total, mail
from flask_mail import Message
from .models import Register, CustomerOrder, Payments
import secrets, os, json, pdfkit
from mollie.api.client import Client


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
            mollie_client = Client()
            mollie_client.set_api_key(os.environ.get('API_KEY'))
            amount = cal_cart_total(session['Shoppingcart'])
            
            payment = mollie_client.payments.create({
                'amount': {
                    'currency': 'EUR',
                    'value': str(amount)
                },
                'description': 'Payment for invoice: ' + invoice,
                'redirectUrl': 'http://verclean-531794983.eu-west-1.elb.amazonaws.com/ordercomplete/' + invoice,
                'webhookUrl': 'https://verclean-531794983.eu-west-1.elb.amazonaws.com/mollie-webhook/',
                'metadata': {
                    'invoice': str(invoice)
                }
            })
        
            if payment.status == 'open':
                payments = Payments(
                    status = payment.status,
                    amount = amount,
                    invoice = invoice,
                    payment_id = payment.id
                )
            
                order = CustomerOrder(
                    invoice = invoice,
                    customer_id = customer_id,
                    orders = session['Shoppingcart']
                )
                
                db.session.add(payments)
                db.session.add(order)
                db.session.commit()
                
                session.pop('Shoppingcart')
                return redirect(payment.checkout_url)
            return redirect(url_for('carts'))
                    
        except Exception as e:
            print(e)
            flash('Something went wrong while getting orders', 'danger')
            return redirect(url_for('get_carts'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        totaldiscount = 0
        grandtotal = 0
        subtotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        tax = 0
        
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))
            totaldiscount += discount
    
    else:
        return redirect(url_for('CustomerLogin'))
    return render_template('customer/orders.html', invoice=invoice, tax=tax, subtotal=subtotal, grandtotal=grandtotal, discount=totaldiscount, customer=customer, orders=orders)


@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        totaldiscount = 0
        grandtotal = 0
        subtotal = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            tax = 0
        
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subtotal += float(product['price']) * int(product['quantity'])
                subtotal -= discount
                tax = ("%.2f" % (.06 * float(subtotal)))
                grandtotal = float("%.2f" % (1.06 * subtotal))
                totaldiscount += discount
  
            rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax, subtotal=subtotal, grandtotal=grandtotal, discount=totaldiscount, customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['Content-Type']='application/pdf'
            response.headers['Content-Disposition']='inline: filename='+ invoice +'.pdf'
            return response
        return request(url_for('orders'))


@app.route('/ordercomplete/<invoice>')
def ordercomplete(invoice):
    try:
        mollie_client = Client()
        mollie_client.set_api_key('test_DH6rG3RrUAQrJGngCPgdzqD8GCE3Kd')
        
        invoice_payment = Payments.query.filter_by(invoice=invoice).first()
        payment = mollie_client.payments.get(invoice_payment.payment_id)
        
        if payment.is_paid():
            invoice_payment.status = payment.status
            db.session.commit()
            return render_template('customer/order_complete.html')

    except Exception as e:
        print(e)


@app.route('/contact', methods=['GET', 'POST'])
def contact(): 
    if request.method == 'GET':
        return redirect(url_for('contactus'))
    if request.method == 'POST': 
           
        firstname = request.form['firstname']
        body = "Mr/Mr " + request.form['firstname'] + firstname + "," + "<br/>" + request.form['message'] + request.form['email']  
        msg = Message(subject=request.form['subject'],
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[app.config.get("RECIPIENT")],
                      body=body)
        mail.send(msg)
        flash(f'Hi {firstname},  thank you for getting in touch with us.')
        return render_template('products/contact.html')