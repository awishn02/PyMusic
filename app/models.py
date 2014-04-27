from sqlalchemy.dialects.mysql import TINYINT, TIMESTAMP, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Feed(Base):
  __tablename__ = "feeds"
  id = Column(Integer, primary_key=True)
  url = Column(String(255), unique=True)
  title = Column(String(255))
  songs = relationship('Song', backref='feeds', lazy='dynamic')

  def __init__(self, url, title):
    self.url = url
    self.title = title

class Song(Base):
  __tablename__ = "songs"
  id = Column(Integer, primary_key=True)
  title = Column(String(255))
  player_id = Column(Integer)
  song_id = Column(String(50), unique=True)
  disliked = Column(Integer, default=0)
  feed_id = Column(Integer, ForeignKey(Feed.id))
  pub_date = Column(DateTime)
  
  def __init__(self, title, player_id, song_id, feed_id, pub_date):
    self.title = title
    self.player_id = player_id
    self.song_id = song_id
    self.feed_id = feed_id
    self.pub_date = pub_date

  def __repr__(self):
    return '<Song title: %r, player: %d, song_id: %r, feed_id: %d>' % (self.title, self.player_id, self.song_id, self.feed_id)
