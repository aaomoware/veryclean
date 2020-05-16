from shop import db
from datetime import datetime

class DeliveryAddress():
    order_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, primary_key=False)
    country = db.Column(db.String(12), nullable=False)
    address1 = db.Column(db.String(240), nullable=False)
    address2 = db.Column(db.String(240), nullable=True)
    province = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    firstname = db.Column(db.String(25), nullable=False)
    company_name = db.Column(db.String(120), nullable=True)
    zippostalcode = db.Column(db.String(8), nullable=False)

class createaccount():
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, primary_key=False)
    country = db.Column(db.String(12), nullable=False)
    address1 = db.Column(db.String(240), nullable=False)
    address2 = db.Column(db.String(240), nullable=True)
    province = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    firstname = db.Column(db.String(25), nullable=False)
    company_name = db.Column(db.String(120), nullable=True)
    zippostalcode = db.Column(db.String(8), nullable=False)
    
class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    colours = db.Column(db.Text(80), nullable=False)
    discount = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='default.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='default.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='default.jpg')

    def __repr__(self):
        return '<Addproduct %r>' % self.name