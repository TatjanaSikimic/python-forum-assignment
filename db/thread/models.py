import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship
from db.connection import Base
from db.user.models import User

@as_declarative()
class Base:
    pass

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

# Example of the table, for the assigment refer to https://docs.sqlalchemy.org/en/14/#
class Thread(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    dtCreated = Column(DateTime, default=datetime.datetime.utcnow)
    # dodati neko ogranicenje da datum updejtovanja ne bude manji od datuma kreiranja?
    dtUpdated = Column(DateTime, default=datetime.datetime.utcnow)
    # CheckConstraint('NOT(@dtUpdated < @dtCreated)')
    user_id = Column(Integer, ForeignKey("user.id"))

    __mapper_args__ = {
        "polymorphic_identity": "thread",
        "polymorphic_on": type,
    }

    def __init__(self, id, title, dt_created, dt_updated, user_id, *args, **kwargs):
        self.id = id
        self.title = title
        self.dtCreated = dt_created
        self.dtUpdated = dt_updated
        self.user_id = user_id

# TODO: Include models that need to be in the database, along with their relationships
# TODO: Check how to get models metadata


