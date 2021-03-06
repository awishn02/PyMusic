from pprint import pprint
from app import app, models, lm, login_serializer, bcrypt
import datetime, time, urllib, urllib2, httplib2, json, re, feedparser, sys, traceback
import flask
from soundclouddownloader import SoundCloudDownload
from flaskext.bcrypt import Bcrypt
from flask import Flask,redirect,request,render_template, g, Response, send_file, make_response
from parser import parse_feed
from feed_to_json import json_handle
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, and_
from forms import FeedForm, LoginForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from database import db_session
from pytube import YouTube
bcrypt = Bcrypt(app)
feedparser.SANITIZE_HTML = False

USER = 0
DOWNLOADER = 1
ADMIN = 2

def to_json_list(results, is_query=False):
  output = []
  for result in results:
    row = {}
    for col in result.__table__.columns:
      if col.name == "pub_date":
        row[col.name] = getattr(result, col.name).strftime("%Y-%m-%d %H:%M:%S")
      else:
        row[col.name] = getattr(result, col.name)
    output.append(row)
  return output

def tryConnection (applyfun):
    try:
        return applyfun()
    except OperationalError:
        print "operation error"
        return applyfun()


@app.route('/')
def index():
  if current_user is not None and current_user.is_authenticated():
    return render_template("index.html", user=current_user)
  form = LoginForm()
  return render_template("index.html", form=form)

@lm.user_loader
def load_user(userid):
  return models.User.query.get(userid)

@lm.token_loader
def load_token(token):
  max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
  data = login_serializer.loads(token, max_age=max_age)
  user = models.User.query.get(data[0])
  if user and data[1] == user.password:
    return user
  return None

@app.route('/login', methods=['POST'])
def login():
  if current_user is not None and current_user.is_authenticated():
    return "already_logged_in"
  email = request.args.get('email')
  password = request.args.get('password')
  remember_me = request.args.get('remember_me')
  user = tryConnection(lambda: models.User.query.filter_by(email=email).first())
  if user is None:
    return "ERROR"
  if not bcrypt.check_password_hash(user.password, password):
    return "ERROR"
  login_user(user, remember=remember_me)
  return "SUCCESS"

@app.route('/register', methods=['POST'])
def register():
  if current_user is not None and current_user.is_authenticated():
    return "already_logged_in"
  email = request.args.get('email')
  password = request.args.get('password')
  remember_me = request.args.get('remember_me')
  user = models.User(email=email, password=bcrypt.generate_password_hash(password))
  db_session.add(user)
  db_session.commit()
  login_user(user, remember=remember_me)
  return "SUCCESS"

@app.route('/admin', methods=['GET'])
@login_required
def admin():
  if current_user is not None and current_user.is_authenticated() and current_user.user_type_id == ADMIN:
    return render_template("admin.html", user=current_user)
  return redirect('/')

@app.route('/get_songs', methods=['GET'])
def get_songs():
  if current_user is not None and current_user.is_authenticated() and current_user.user_type_id == ADMIN:
    return render_template("songs.html", user=current_user)
  return render_template('songs.html')

@app.route('/users', methods=['GET'])
@login_required
def user_list():
  if current_user is not None and current_user.is_authenticated() and current_user.user_type_id == ADMIN:
    users = models.User.query.all()
    return json.dumps(to_json_list(users))
  return redirect('/')

@app.route('/logout')
def logout():
  logout_user()
  return redirect("/")

@app.route('/scdownload', methods=['POST'])
def scdownload():
  url = request.args.get('url')
  download = SoundCloudDownload(url, False, False)
  f = download.downloadSongs()
  filename = "/static/"+f.split('/')[2]
  return filename

@app.route('/ytdownload', methods=['POST'])
def ytdownload():
  url = request.args.get('url')
  yt = YouTube()
  yt.url = url
  video = yt.filter('mp4')[0]
  return "/static/"+video.download().split('/')[2]


#################
## RESTFUL API ##
#################

@app.route('/posts', methods=['GET'])
def posts():
  try:
    feeds = models.Feed.query.all()
    for feed in feeds:
      url = feed.url
      data = parse_feed(url)
      for d in data:
        s = models.Song.query.filter_by(song_id=d['song_id']).first()
        if s is None:
          song = models.Song(title=d['title'], player_id=d['player_id'],
              song_id=d['song_id'], feed_id=feed.id, pub_date=d['pub_date'])
          db_session.add(song)
    db_session.commit()
    return "Success"
  except IntegrityError as e:
    pass
  except Exception as e:
    return "Error: " + str(e)

@app.route('/songs', methods=['GET'])
def songs():
  feed_id = request.args.get('feed_id')
  if current_user is not None and current_user.is_authenticated():
    dislikes = current_user.dislikes
    no_include = and_( *[models.Song.id != x.id for x in dislikes])
    if feed_id is not None:
      songs = models.Song.query.filter_by(disliked=0,feed_id=feed_id).filter(no_include).order_by(desc(models.Song.pub_date)).all()
    else:
      songs = models.Song.query.filter_by(disliked=0).filter(no_include).order_by(desc(models.Song.pub_date)).all()
  else:
    if feed_id is not None:
      songs = models.Song.query.filter_by(disliked=0,feed_id=feed_id).order_by(desc(models.Song.pub_date)).all()
    else:
      songs = models.Song.query.filter_by(disliked=0).order_by(desc(models.Song.pub_date)).all()
  return json.dumps(to_json_list(songs))

@app.route('/delete_songs', methods=['GET'])
def del_songs():
  songs = models.Song.query.all()
  for song in songs:
    db_session.delete(song)
  db_session.commit()
  return 'All songs deleted'

@app.route('/drop_all')
def drop_all():
  # db.drop_all()
  return "Dropped"

@app.route('/feeds', methods=['GET','POST'])
def feed():
  form = FeedForm()
  if form.validate_on_submit():
    feed = models.Feed(url=form.url.data,title=form.title.data)
    db_session.add(feed)
    db_session.commit()
    return redirect('/')
  return render_template('feed.html',form=form)

@app.route('/feeds.json', methods=['GET'])
def feedJSON():
  search = request.args.get('search')
  if search is not None:
    feeds = db_session.query(models.Feed).filter(models.Feed.title.ilike('%'+search+'%')).all()
    return json.dumps(to_json_list(feeds))
  all_req = request.args.get('all')
  if current_user is not None and current_user.is_authenticated() and current_user.feeds.first() is not None and all_req is None:
    return json.dumps(to_json_list(current_user.feeds.all()))
  feeds = models.Feed.query.all()
  return json.dumps(to_json_list(feeds))

@app.route('/favorite', methods=['POST'])
@login_required
def favorite():
  try:
    user_id = request.args.get('user_id')
    feed_id = request.args.get('feed_id')
    print user_id, feed_id
    user = models.User.query.get(user_id)
    feed = models.Feed.query.get(feed_id)
    if feed is not None:
      if not db_session.query(models.users_has_feeds).filter_by(users_id=user_id,feeds_id=feed_id).first():
        user.feeds.append(feed)
        db_session.commit()
      return json.dumps({"success": True})
  except Exception, err:
    print traceback.format_exc()
    return json.dumps({"success": False})

@app.route('/dislike', methods=['POST'])
@login_required
def dislike():
  try:
    user_id = request.args.get('user_id')
    song_id = request.args.get('song_id')
    user = models.User.query.get(user_id)
    song = models.Song.query.get(song_id)
    if song is not None:
      if not db_session.query(models.users_dislikes_songs).filter_by(users_id=user_id,songs_id=song_id).first():
        user.dislikes.append(song)
        db_session.commit()
      return json.dumps({"success":True})
  except Exception, err:
    print err
    return json.dumps({"success":False})
