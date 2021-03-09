from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart', methods=['POST'])
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
