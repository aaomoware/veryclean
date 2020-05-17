from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=False)
    lastname = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), unique=False)
    country = db.Column(db.String(50), unique=False)
    postcode = db.Column(db.String(50), unique=False)
    companyname = db.Column(db.String(100), unique=False)
    address1 = db.Column(db.String(200), unique=False)
    address2 = db.Column(db.String(200), unique=False)
    province = db.Column(db.String(100), unique=False)
    towncity = db.Column(db.String(100), unique=False)
    phonenumber = db.Column(db.Integer, unique=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Register %r>' % self.name


class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text
    
    def set_value(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    
    def get_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEncodedDict)
    
    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice


db.create_all()
    