import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_msearch import Search
from flask_login import LoginManager, login_manager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('user_sqlite')#in this variable you have to put the data of your db example > 'sqlite:///shop.db'	
app.config['SECRET_KEY'] = os.environ.get('password_sqlite')   		 #in this variable you have to put the data of your db example > 'asddsaasd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'CustomerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'Please login first'


from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
