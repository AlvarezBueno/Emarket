from shop import db

from datetime import datetime


class Addproduct(db.Model):  # Añadir producto y caracteristicas a la BBDD
    __searchable__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    cost = db.Column(db.Numeric(10, 2))
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    sells = db.Column(db.Integer, nullable=True)
    colors = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Post %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=True, unique=True)
    email = db.Column(db.String, nullable=True, unique=True)
    address = db.Column(db.String, nullable=True, unique=True)
    CIF = db.Column(db.String, nullable=True, unique=True)
    IVA = db.Column(db.Integer, nullable=True, unique=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


db.create_all()
