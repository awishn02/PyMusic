from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
feed = Table('feed', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String(length=255)),
)

song = Table('song', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=255)),
    Column('player_id', Integer),
    Column('song_id', String(length=50)),
    Column('disliked', Integer, default=ColumnDefault(0)),
    Column('feed_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feed'].create()
    post_meta.tables['song'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feed'].drop()
    post_meta.tables['song'].drop()
