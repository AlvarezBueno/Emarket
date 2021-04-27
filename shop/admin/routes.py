from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, Addbrands
from .models import User
from shop.products.models import Addproduct, Brand, Category
from flask_login import login_required, current_user, logout_user, login_user
import os


@app.route("/admin")
def admin():
    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin page', products=products)


@app.route('/brands', methods=['GET', 'POST'])  # Administrador.
def brands():
    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))

    form = Addbrands(request.form)
    if request.method == "POST":
        phone = form.phone.data
        email = form.email.data
        address = form.address.data
        CIF = form.CIF.data
        IVA = form.IVA.data
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand, phone=phone, email=email, address=address, CIF=CIF, IVA=IVA)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('brands', form=form))

    elif request.method == 'GET':
        brands = Brand.query.order_by(Brand.id.desc()).all()
        return render_template('admin/brand.html', title="Brand page", brands=brands, form=form)


@app.route('/brands/<int:id>', methods=['PUT', 'DELETE'])
def brand(id):
    brand = Brand.query.get_or_404(id)

    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))

    elif request.method == "PUT":
        updatebrand = request.form.get('brand')
        brand.name = updatebrand
        flash(f'La marca ha sido actualizada', 'success')

    elif request.method == "DELETE":
        db.session.delete(brand)
        flash(f'La marca ha sido eliminada de la base de datos', 'success')

    db.session.commit()
    return redirect(url_for('brands'))


@app.route('/category', methods=['GET', 'POST'])
def categories():
    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'La categoria {getcategory} ha sido añadida a tu base de datos', 'success')
        db.session.commit()
        return redirect(url_for('categories'))

    elif request.method == 'GET':
        categories = Category.query.order_by(Category.id.desc()).all()
        return render_template('admin/category.html', title="Category page", categories=categories)


@app.route('/category/<int:id>', methods=['PUT', 'DELETE'])
def category(id):
    category = Category.query.get_or_404(id)

    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))

    elif request.method == "PUT":
        updatecategory = request.form.get('category')
        category.name = updatecategory
        flash(f'La marca ha sido actualizada', 'success')

    elif request.method == "DELETE":
        db.session.delete(category)
        flash(f'La categoria ha sido eliminada de la base de datos', 'success')

    db.session.commit()
    return redirect(url_for('category'))


@app.route('/registeradmin', methods=['GET', 'POST'])  # accesible solo por cuestiones de desarrollo
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print("hola")
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Bienvenido, {form.name.data}, Gracias por registrarte', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Register page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Bienvenido {form.email.data} has iniciado sesión correctamente', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong password, please try again', 'danger')

    return render_template('admin/login.html', form=form, title='Login Page')


@app.route('/admin/logout')
def admin_logout():
    logout_user()
    return render_template('products/index.html')
