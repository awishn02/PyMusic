from pprint import pprint
from app import app, models, lm, login_serializer
import datetime, time, urllib, urllib2, httplib2, json, re, feedparser, sys
import flask
from flaskext.bcrypt import Bcrypt
from flask import Flask,redirect,request,render_template, g
from parser import parse_feed
from feed_to_json import json_handle
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from forms import FeedForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from database import db_session
bcrypt = Bcrypt(app)
feedparser.SANITIZE_HTML = False

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


@app.route('/')
def index():
  return render_template("index.html")


#################
## RESTFUL API ##
#################

@app.route('/posts', methods=['GET'])
def posts():
  try:
    feeds = models.Feed.query.all()
    for feed in feeds:
      print feed.url
      url = feed.url
      data = parse_feed(url)
      for d in data:
        s = models.Song.query.filter_by(song_id=d['song_id']).first()
        print s
        if s is None:
          song = models.Song(title=d['title'], player_id=d['player_id'],
              song_id=d['song_id'], feed_id=feed.id, pub_date=d['pub_date'])
          db_session.add(song)
    db_session.commit()
    return "Success"
  except IntegrityError as e:
    pass
  except Exception as e:
    return str(e)

@app.route('/songs', methods=['GET'])
def songs():
  feed_id = request.args.get('feed_id')
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
  feeds = models.Feed.query.all()
  return json.dumps(to_json_list(feeds))
