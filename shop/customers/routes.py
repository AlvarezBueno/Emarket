from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import db, app, photos, bcrypt
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register
import secrets  # reasigna nombres a los archivos subidos como fotos u otros.
import os

# --NO FUNCIONAL. EN DESARROLLO. Problemas con la session.--


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
                            password=hash_password, country=form.country.data, state=form.state.data,
                            city=form.city.data, address=form.address.data, zipcode=form.zipcode.data,
                            contact=form.contact.data)  # Ignorar error. Por alguna razón da el metodo como inaccesible. Pero funciona.
        db.session.add(register)
        flash(f"Bienvenido{form.name.data} Gracias por registrarte", 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'¡Bienvenido {form.email.data}!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home', form=form))
        flash('contraseña o usuario incorrectos', 'danger')
        return redirect(url_for('customerLogin', form=form))

    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customer_login'))
