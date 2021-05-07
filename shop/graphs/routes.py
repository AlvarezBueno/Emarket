import io

import matplotlib
import sqlite3
import numpy as np

import matplotlib.pyplot as plt
from shop import app, db
from shop.products.models import Addproduct

from flask import Response, render_template
from calendar import monthrange
from matplotlib.pyplot import figure

import base64
from io import BytesIO


@app.route('/plot.png/<int:id>')
def grafico(id):
    product = Addproduct.query.get_or_404(id)
    conexion = sqlite3.connect("shop/db.db")
    cursor = conexion.cursor()

    fechado = []
    vendido = []
    import datetime
    now = datetime.datetime.now()
    month = monthrange(now.year, now.month)
    for day in range(1, month[1]):
        if day > now.day:
            break
        x = datetime.datetime(now.year, now.month, day)
        date = x.strftime("%Y %m %d")
        query = "SELECT SUM(quantity) FROM ventas WHERE id = '" + str(id) + "' AND date = '" + date + "'"
        ventas = cursor.execute(query)
        quantity = ventas.fetchall()
        q = quantity[0][0] or 0  # Necesario o la query dará valores NULL
        fechado.append(date)
        vendido.append(q)
    print(fechado)
    print(vendido)

    figure(figsize=(8, 6), dpi=120)
    x = np.array(range(0, len(fechado)))  # Hay que determinar cuantos "ticks" hay para poder asignarles las fechas.
    y = np.array(vendido)
    plt.ylabel('Unidades Vendidas')
    plt.xticks(x, fechado, rotation=45, fontsize=8)
    plt.title("Evolución mensual de ventas para: " + product.name)
    plt.plot(x, y)
    output = io.BytesIO()
    plt.savefig(output, format='png')
    matplotlib.use('agg')
    plt.close()  # importante o se acumulan los graficos en el output.
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/graph/<int:id>')
def graph(id):
    product = Addproduct.query.get_or_404(id)

    return render_template('products/graph.html', product=product)

