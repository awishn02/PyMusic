from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

class FeedForm(Form):
  url = TextField('url', validators=[Required()])
  title = TextField('title', validators=[Required()])

class LoginForm(Form):
  email = TextField('email', validators=[Required()])
  password = PasswordField('password', validators=[Required()])
  remember_me = BooleanField('remember_me')
