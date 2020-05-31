from flask import redirect, render_template, flash, request, url_for, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, cal_cart
import json
from decimal import Decimal
from shop.products.models import Addproduct

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
        return redirect(url_for('shop'))
    tax, subtotal, grandtotal, totaldiscount, post_cost = cal_cart(session['Shoppingcart'])
    return render_template('products/cart.html', tax=tax, grandtotal=grandtotal, totaldiscount=totaldiscount, subtotal=subtotal, post_cost=post_cost)


@app.route('/clearcart', methods=['POST'])
def clearcart():
    if request.method == 'POST':
        try:
            session.pop('Shoppingcart', None)
            return redirect(url_for('shop'))
        except Exception as e:
            print(e)



@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    if request.method == 'POST':
        tax, subtotal, grandtotal, totaldiscount, post_cost = cal_cart(session['Shoppingcart'])
        return render_template('products/checkout.html', tax=tax, grandtotal=grandtotal, totaldiscount=totaldiscount, subtotal=subtotal, post_cost=post_cost)
    else:
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