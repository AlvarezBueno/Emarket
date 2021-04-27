import io
from shop import app
from shop.products.models import Addproduct
from shop.products.forms import Addproducts
from flask import Flask
from flask import Response

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@app.route('/plot.png')
def dibuja_grafico():
    con = Addproduct.query.get_or_404(id)
    prod = con.name
    cant = con.stock
    cantidad = []
    productos = []
    for n in prod:
        productos.append(n)
    for n in cant:
        cantidad.append(n)
    df = pd.DataFrame({
        'nombre': productos,
        'Cantidad': cantidad,

    })

    df.plot(figsize=(16, 4), title='Gráfico de ejemplo', kind='bar', stacked=False)
    output = io.BytesIO()
    plt.legend()
    plt.savefig(output, format='png')
    return Response(output.getvalue(), mimetype='image/png')