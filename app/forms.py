from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class FeedForm(Form):
  url = TextField('url', validators=[Required()])
  title = TextField('title', validators=[Required()])
