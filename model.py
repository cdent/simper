""" The basic data model for what we're fiddling with here.
    Based on Joe Gregorio's
    http://bitworking.org/news/Why_so_many_Python_web_frameworks
"""

from datetime import datetime
from sqlalchemy import Table, Column, String, Integer, DateTime, ForeignKey
import dbconfig

type_list_table = Table('type_list', dbconfig.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), index=True),
)

revision_table = Table('revision', dbconfig.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('content_type', String(50), index=True),
        Column('content_uri', String(200), index=True),
        Column('mod_time', DateTime, default=datetime.now),
)

type_table = Table('type', dbconfig.metadata,
        Column('type_id', Integer, ForeignKey("type_list.id"), index=True),
        Column('revision_id', Integer, ForeignKey("revision.id"), index=True),
)

content_table = Table('content', dbconfig.metadata,
        Column('id', Integer, ForeignKey("revision.id"), index=True),
        Column('name', String(100), index=True),
)

association_table = Table('association', dbconfig.metadata,
        Column('from_id', Integer, ForeignKey("revision.id"), index=True),
        Column('to_id', Integer, ForeignKey("revision.id"), index=True),
)
