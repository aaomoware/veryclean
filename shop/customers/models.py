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
        return '<Register %r>' % self.firstname


class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
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
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice


class Payments(db.Model):
    status = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    invoice = db.Column(db.String(20), primary_key=True)
    payment_id = db.Column(db.String(100), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


db.create_all()
    

