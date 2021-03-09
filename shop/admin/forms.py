from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField


class RegistrationForm(Form):
    name = StringField('Nombre', [validators.Length(min=4, max=25)])
    username = StringField('Nombre de Usuario', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Contraseña', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Ambas contraseñas deben coincidir')
    ])
    confirm = PasswordField('Repita la contraseña')


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Contraseña', [validators.DataRequired()])


class Addbrands(Form):
    phone = StringField('Telefono:', [validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    address = StringField('Direccion:', [validators.DataRequired()])
    CIF = StringField('CIF:', [validators.DataRequired(), validators.Length(min=8, max=9)])
    IVA = StringField('IVA:', [validators.DataRequired()])