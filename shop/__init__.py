from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_mail import Mail
import os
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))
secret_key = os.environ.get('SECRET_KEY', 'ljoljd8dsnecsk8g38asn93=--93')

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['MAIL_USERNAME'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD'],
    "MAIL_RECIPIENT": os.environ['MAIL_RECIPIENT']
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = secret_key
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config.update(mail_settings)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

def cal_cart(orders):
    tax = 0
    subtotal = 0
    grandtotal = 0
    totaldiscount = 0
    
    for key, product in orders.items():
        discount = (product['discount']/100 * float(product['price']))
        totaldiscount += discount
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.21 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))

    amount = str(tax).split(".")
    if len(amount[1]) < 1:
        tax = amount[0] + '.' + amount[1] + '0'  
    amount = str(subtotal).split(".")
    if len(amount[1]) < 1:
        subtotal = amount[0] + '.' + amount[1] + '0'
    amount = str(grandtotal).split(".")
    if len(amount[1]) < 1:
        grandtotal = amount[0] + '.' + amount[1] + '0'
    amount = str(totaldiscount).split(".")
    if len(amount[1]) < 1:
        totaldiscount = amount[0] + '.' + amount[1] + '0' 
    
    return tax, subtotal, grandtotal, totaldiscount


def cal_cart_total(orders):
    discount = 0
    subtotal = 0
    grandtotal = 0
    
    for key, product in orders.items():
        discount = (product['discount']/100 * float(product['price']))
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        grandtotal = float("%.2f" % (1.06 * subtotal))
    
    amount = str(grandtotal).split(".")
    if len(amount[1]) < 1:
        grandtotal = amount[0] + '.' + amount[1] + '0'
        return grandtotal
    return grandtotal
        
        
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"

mail = Mail(app)

from shop.admin import routes
from shop.products import routes
from shop.carts import routes
from shop.customers import routes
