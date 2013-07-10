from sqlalchemy import *

metadata = MetaData()

data = Table('data', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('type', String(8)),
    Column('date', Date),
    Column('value', Integer),

    Index('u1', 'user_id', 'type', 'date', unique=True)
)
