import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = None

try:
  from config import SQLALCHEMY_DATABASE_URI
  engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
except ImportError:
  engine = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)
  pass

session = sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine)
session._model_changes = {}
db_session = scoped_session(session)
db_session = session

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
