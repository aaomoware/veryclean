from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'ljoljd8dsnecsk8g38asn93=--93'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def cal_cart(orders):
    tax = 0
    subtotal = 0
    grandtotal = 0
    totaldiscount = 0
    totalsubtotal = 0
    
    for key, product in orders.items():
        discount = (product['discount']/100 * float(product['price']))
        totaldiscount += discount
        subtotal += float(product['price']) * int(product['quantity'])
        totalsubtotal += float(product['price']) * int(product['quantity']) 
        subtotal -= discount
        tax = ("%.2f" % (.21 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return totalsubtotal, grandtotal, totaldiscount, subtotal, tax

def cal_cart_total(orders):
    tax = 0
    subtotal = 0
    grandtotal = 0
    totaldiscount = 0
    totalsubtotal = 0
    
    for key, product in orders.items():
        discount = (product['discount']/100 * float(product['price']))
        totaldiscount += discount
        subtotal += float(product['price']) * int(product['quantity'])
        totalsubtotal += float(product['price']) * int(product['quantity']) 
        subtotal -= discount
        tax = ("%.2f" % (.21 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return grandtotal
        
        
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
