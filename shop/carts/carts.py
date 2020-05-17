from flask import redirect, render_template, flash, request, url_for, session, current_app
from flask_login import current_user, logout_user, login_user
from shop import db, app
import json
from decimal import Decimal
from shop.products.models import Addproduct
from shop.customers.models import Register

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return false

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        quantity = request.form.get('quantity')
        product_id = request.form.get('product_id')
        product = Addproduct.query.filter_by(id=product_id).first()
        
        if request.method == 'POST':
            product_price = str(Decimal(product.price))
            DictItems = {product_id: {'name': product.name, 'price': product_price, 'discount': product.discount, 
            'quantity': quantity, 'image': product.image_1}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] = int(item['quantity']) + 1
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def get_carts():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    tax = 0
    subtotal = 0
    grandtotal = 0
    totaldiscount = 0
    totalsubtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100 * float(product['price']))
        totaldiscount += discount
        subtotal += float(product['price']) * int(product['quantity'])
        totalsubtotal += float(product['price']) * int(product['quantity']) 
        subtotal -= discount
        tax = ("%.2f" % (.21 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('products/cart.html', tax=tax, grandtotal=grandtotal, totaldiscount=totaldiscount, subtotal=subtotal)


@app.route('/clearcart', methods=['POST'])
def clearcart():
    if request.method == 'POST':
        try:
            session.pop('Shoppingcart', None)
            return redirect(url_for('shop'))
        except Exception as e:
            print(e)



@app.route('/checkout', methods=['POST'])
def checkout():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    if request.method == 'POST':
        
        if current_user.is_authenticated:
            user = True
        else:
            user = False
            
        tax = 0
        subtotal = 0
        grandtotal = 0
        totaldiscount = 0
        totalsubtotal = 0
        for key, product in session['Shoppingcart'].items():
            discount = (product['discount']/100 * float(product['price']))
            totaldiscount += discount
            subtotal += float(product['price']) * int(product['quantity'])
            totalsubtotal += float(product['price']) * int(product['quantity']) 
            subtotal -= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))
        return render_template('products/checkout.html', tax=tax, grandtotal=grandtotal, totaldiscount=totaldiscount, subtotal=subtotal, user=user)
    else:
        return redirect(url_for('shop'))



@app.route('/placeorder', methods=['POST'])
def placeorder():
    try:
        if request.method == 'POST':
            country = request.form.get('country')
            address1 = request.form.get('address1')
            address2 = request.form.get('address2')
            province = request.form.get('province')
            lastname = request.form.get('lastname')
            firstname = request.form.get('firstname')
            company_name = request.form.get('company_name')
            zippostalcode = request.form.get('zippostalcode')
            createaccount = request.form.get('createaccount')
            onlyfordelivery = request.form.get('onlyfordelivery')            
            return render_template('products/order_complete.html')
        else:
            return redirect(url_for('shop'))
    except Exception as e:
        print(e)
        return redirect(url_for('shop'))


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('shop'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash(f'Product has been updated successfully')
                    return redirect(url_for('get_carts'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_carts'))
        

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('shop'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('get_carts'))
    except Exception as e:
        print(e)
        return redirect(url_for('get_carts'))