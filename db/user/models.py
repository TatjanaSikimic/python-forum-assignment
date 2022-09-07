import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship
from db.connection import Base
from db.thread.models import Thread

from . import hashing

@as_declarative()
class Base:
    pass

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

# Example of the table, for the assigment refer to https://docs.sqlalchemy.org/en/14/#
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255))
    signature = Column(String(50))
    threads = relationship('Thread', backref='thread', lazy='dynamic')

    def __init__(self, id, name, username, password, avatar, signature, *args, **kwargs):
        self.id = id
        self.name = name
        self.username = username
        self.password = hashing.get_password_hash(password)
        self.avatar = avatar
        self.signature = signature

    def check_password(self, password):
        return hashing.verify_password(self.password, password)

# TODO: Include models that need to be in the database, along with their relationships
# TODO: Check how to get models metadata

