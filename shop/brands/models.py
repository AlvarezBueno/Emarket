from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return Brand.query.get


class Brand(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False)
    state = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    contact = db.Column(db.String(50), primary_key=True)
    address = db.Column(db.String(50), unique=False)
    zipcode = db.Column(db.String(50), unique=False)
    CIF = db.Column(db.String(9), nullable=True, unique=True)
    IVA = db.Column(db.Integer, nullable=True, unique=False)

    def __repr__(self):
        return '<Register %r>' % self.name


db.create_all()
