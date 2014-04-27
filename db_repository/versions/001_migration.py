from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Users = Table('Users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=255), nullable=False),
    Column('email', VARCHAR(length=255), nullable=False),
    Column('password', VARCHAR(length=255), nullable=False),
    Column('status', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Users'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Users'].create()
