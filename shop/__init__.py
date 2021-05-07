from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_login import LoginManager
from flask_msearch import Search

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = "cdkil1k12h31hlasdj"  # al azar, no importa. la cosa es poner algo.
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)  # inicializacion de la funcion search.

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresg_message_category = 'danger'
login_manager.login_message = "Conectese por favor"

from shop.admin import routes
from shop.products import routes
from shop.carts import cart
from shop.customers import routes
from shop.Marcas import routes
from shop.graphs import routes
