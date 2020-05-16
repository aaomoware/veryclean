from shop import db
from datetime import datetime

class Register(db.Model):
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
    phonenumber = db.Column(db.Integer, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Register %r>' % self.name

db.create_all()
    