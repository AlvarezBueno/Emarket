from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import db, app, photos, bcrypt
from flask_login import login_required, current_user, logout_user, login_user
from .forms import MarcaRegisterForm, MarcaLoginForm
from .models import Marca
import secrets  # reasigna nombres a los archivos subidos como fotos u otros.
import os


@app.route('/marcas/register', methods=['GET', 'POST'])
def brand_register():
    form = MarcaRegisterForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Marca(name=form.name.data, email=form.email.data,
                            password=hash_password, country=form.country.data, state=form.state.data,
                            city=form.city.data, address=form.address.data, zipcode=form.zipcode.data,
                            contact=form.contact.data, CIF=form.CIF.data, IVA=form.IVA.data)  # Ignorar error. Por alguna razón da el metodo como inaccesible. Pero funciona.
        db.session.add(register)
        flash(f"Bienvenido{form.name.data} Gracias por registrarte", 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('marcas/register.html', form=form)


@app.route('/marcas/login', methods=['GET', 'POST'])
def marca_login():
    form = MarcaLoginForm()
    if form.validate_on_submit():
        userbrand = Marca.query.filter_by(email=form.email.data).first()
        if userbrand and bcrypt.check_password_hash(userbrand.password, form.password.data):
            login_user(userbrand)
            flash(f'¡Bienvenido {form.email.data}!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home', form=form))
        flash('contraseña o usuario incorrectos', 'danger')
        return redirect(url_for('customerLogin', form=form))

    return render_template('marcas/login.html', form=form)


@app.route('/customer/logout')
def marca_logout():
    logout_user()
    return redirect(url_for('customerLogin'))
