from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

"""class ProductImage:
    def __init__(self, name):
        self.name = name
        FileField(self.name, validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg']),
                                         'Solo imagenes por favor'])"""


class Addproducts(Form):
    name = StringField('Nombre:', [validators.DataRequired()])
    price = DecimalField('Precio clientes:', [validators.DataRequired()])
    cost = DecimalField('Coste:', [validators.DataRequired()])
    discount = IntegerField('Descuento:', default=0)
    sells = IntegerField()
    stock = IntegerField('Cantidad:', [validators.DataRequired()])
    description = TextAreaField('Descripcion:', [validators.DataRequired()])
    colors = TextAreaField('Colores:', [validators.DataRequired()])

    image_1 = FileField('Imagen 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Imagen 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Imagen 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

