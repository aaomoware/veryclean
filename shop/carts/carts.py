from flask import redirect, render_template, flash, request, url_for, session, current_app
from shop import db, app
from shop.products.models import Addproduct


@app.route('/addcart', methods=['POST'])
def AddCart():
    quanity = request.form.get('quantity')
    product_id = request.form.get('product_id')
    product = Addproduct.query.filter_by(id=product_id).first()
    
    if product_id and quanity and request.method == 'POST':
        DictItems = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount, 
        'quantify': quanity, 'image': product.image_1}}

        if 'Shoppingcart' in session:
            print(session['Shoppingcart'])
        else:
            session['Shoppingcart'] = DictItems
            return redirect(request.referrer)
    return redirect(request.referrer)