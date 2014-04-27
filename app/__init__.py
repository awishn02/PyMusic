from flask import Flask
from flaskext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer
from config import SQLALCHEMY_DATABASE_URI
app = Flask(__name__)
from sqlalchemy import create_engine
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.secret_key = "THISISASUPERSECRETKEY"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
login_serializer = URLSafeTimedSerializer(app.secret_key)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "/"
from app import views, models
from database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
