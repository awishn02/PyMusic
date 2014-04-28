import os
from flask import Flask
from flaskext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer
app = Flask(__name__)
from sqlalchemy import create_engine
try:
  from config import SQLALCHEMY_DATABASE_URI
  app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
except ImportError:
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
  pass

app.secret_key = "THISISASUPERSECRETKEY"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
login_serializer = URLSafeTimedSerializer(app.secret_key)
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
from app import views, models
from database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
