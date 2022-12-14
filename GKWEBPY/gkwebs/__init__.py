import cloudinary
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel

app = Flask(__name__)
app.secret_key = 'dsdsd^%^^ffdfdfdfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/webhc?charset=utf8mb4' % quote('huyzxv123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'
cloudinary.config(cloud_name='ddxdyumr9', api_key='214966595867338', api_secret='eIWhOUHzWdYNrChx651h2cvgqGk')
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)
@babel.localeselector
def load_locale():
    return "vi"
