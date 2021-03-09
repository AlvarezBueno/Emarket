from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField, \
    PasswordField, SubmitField, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from .model import Register


class CustomerRegisterForm(Form):
    name = StringField('Nombre: ')
    username = StringField('Usuario: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Contraseña: ', [validators.DataRequired(), validators.EqualTo('confirm',
               message="Ambas contraseñas deben coincidir")])
    confirm = PasswordField('Repita Contraseña: ', [validators.DataRequired()])
    country = StringField('Pais: ', [validators.DataRequired()])
    state = StringField('Region: ', [validators.DataRequired()])
    city = StringField('Ciudad: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Direccion: ', [validators.DataRequired()])
    zipcode = StringField('codigo postal: ', [validators.DataRequired()])

    submit = SubmitField('Register')


def validate_username(self, username):
    if Register.query.filter_by(username=username.data):
        raise ValidationError("Usuario ya registrado")


def validate_email(self, email):
    if Register.query.filter_by(email=email.data):
        raise ValidationError("email ya registrado")


class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    submit = SubmitField("Login")
