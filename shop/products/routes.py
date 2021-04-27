from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import db, app, photos, search
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets  # reasigna nombres a los archivos subidos como fotos u otros.
import os

ROWS_PER_PAGE = 4


@app.route('/')  # Mostrar productos a usuarios, pagina inicio
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=ROWS_PER_PAGE)
    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)


@app.route('/brands/<id>', methods=['GET'])
def userBrand(id):
    Brand.query.get_or_404(id)

    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter_by(brand_id=id).paginate(page=page, per_page=ROWS_PER_PAGE)
    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('products/index.html', brands=brands, categories=categories, products=products)


@app.route('/category/<int:id>', methods=['GET'])
def userCategory(id):
    Category.query.get_or_404(id)

    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter_by(category_id=id).paginate(page=page, per_page=ROWS_PER_PAGE)
    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('products/index.html', brands=brands, categories=categories, products=products)


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('products/single_page.html', product=product, categories=categories, brands=brands)


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'La categoria ha sido actualizada', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update category', updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    try:
        if request.method == "POST":
            db.session.delete(category)
            db.session.commit()
            flash(f'La marca ha sido eliminada de la base de datos', 'success')
            return redirect(url_for('category'))
    except:
        flash(f'La marca no ha podido ser eliminada', 'danger')
        return redirect(url_for('admin'))


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        brand = request.form.get("brand")
        category = request.form.get("category")
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors,
                            description=description, brand_id=brand, category_id=category, image_1=image_1,
                            image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f"The product {name} has been added to your Database", 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', title="Añadir Producto", form=form, brands=brands,
                           categories=categories)


@app.route("/updateproduct/<int:id>", methods=["GET", "POST"])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Inicie sesion antes, por favor', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f"The product {product.name} has been updated", 'success')
        return redirect("/admin")

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description

    return render_template("products/updateproduct.html", form=form, brands=brands, categories=categories,
                           product=product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    try:
        if request.method == "POST":
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
            except Exception as e:
                print(e)

            db.session.delete(product)
            db.session.commit()
            flash(f"El producto {product.name} ha sido eliminado", 'success')
            return redirect(url_for('admin'))
    except:
        flash(f"No ha podido eliminarse el producto:{product.name} ", 'danger')
        return redirect(url_for('admin'))


@app.route('/result')  # busqueda/search
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name', 'description'], limit=3)
    return render_template('products/result.html', products=products)
