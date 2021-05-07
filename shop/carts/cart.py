from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_wtf import form
from shop import db, app
from shop.products.models import Addproduct
from shop.products.forms import Addproducts
import sqlite3
from datetime import datetime, date, time, timedelta


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart/<int:id>')
def AddCart(id):
    print("haciendo cosas")
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    product.stock -= 1
    product.sells += 1

    db.session.commit()
    flash(f"{product.name} comprado", 'success')

    #return redirect(request.referrer)

    #TABLA DE VENTAS
    #Crear/Abrir documento.
    conexion = sqlite3.connect("shop/db.db")
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ventas (id INTEGER, product VARCHAN(100), quantity INTEGER, date INTEGER)")
    venta = [(product.id, product.name, 1)]

    cursor.executemany("INSERT INTO ventas VALUES (?,?,?, strftime('%Y %m %d', 'now') )", venta)
    conexion.commit()
    conexion.close()

    return redirect(request.referrer)


"""@app.route('/addcart', methods=['POST'])
def AddCart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    colors = request.form.get('quantity')
    product = Addproduct.query.filter_by(id=product_id).first()

    if 'Shoppingcart' not in session:
        session['Shoppingcart'] = {}

    # If the product is not in the cart, then add it.
    if not any(product_id in d for d in session['Shoppingcart']):
        session['Shoppingcart'][product_id] = {
                "name": product.name,
                "price": product.price,
                "discount": product.discount,
                "color": colors,
                "quantity": quantity,
                "image": product.image_1
                }

    print(session['Shoppingcart'])

    return redirect(request.referrer)
"""

"""@app.route('/addcart', methods=['POST'])
def AddCart():
    if 'Shoppingcart' not in session:
        session['Shoppingcart'] = {}
        print("e1")

    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('quantity')
        product = Addproduct.query.filter_by(id=product_id).first()

        if product and quantity and colors and request.method == "POST":
            session['Shoppingcart'].append({
                {
                    "name": product.name,
                    "price": product.price,
                    "discount": product.discount,
                    "color": colors,
                    "quantity": quantity,
                    "image": product.image_1
                }
            })
            print("e2")

        if 'Shoppingcart' in session:
            print(session['Shoppingcart'])
        else:
            return redirect(request.referrer)

    except Exception as e:
        print(e)

    finally:
        return redirect(request.referrer)"""


@app.route('/carts')
def getCart():
    if 'Shoppincart' not in session:
        return redirect(request.referrer)
    return render_template('products/carts.html')
