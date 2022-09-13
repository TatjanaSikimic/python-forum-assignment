import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship
from db.connection import Base
import db.hashing

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html


# Example of the table, for the assigment refer to https://docs.sqlalchemy.org/en/14/#
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50))
    username = Column(String(50), unique=True)
    password = Column(String(255))
    avatar = Column(String(255))
    signature = Column(String(50))
    threads = relationship('Thread', secondary='user_thread_link')

    def __init__(self, id, name, username, password, avatar, signature, *args, **kwargs):
        self.id = id
        self.name = name
        self.username = username
        self.password = db.hashing.get_password_hash(password)
        self.avatar = avatar
        self.signature = signature

    def check_password(self, password):
        return db.hashing.verify_password(self.password, password)

class Thread(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String(255))
    dtCreated = Column(DateTime, default=datetime.datetime.utcnow)
    # dodati neko ogranicenje da datum updejtovanja ne bude manji od datuma kreiranja?
    dtUpdated = Column(DateTime, default=datetime.datetime.utcnow)
    # CheckConstraint('NOT(@dtUpdated < @dtCreated)')
    users = relationship('User', secondary='user_thread_link')

    def __init__(self, id, title, dt_created, dt_updated, *args, **kwargs):
        self.id = id
        self.title = title
        self.dtCreated = dt_created
        self.dtUpdated = dt_updated

class User_Thread_Link(Base):
   __tablename__ = 'user_thread_link'

   users_id = Column(Integer,
                     ForeignKey('users.id'),
                     primary_key=True,
                     unique=True)

   thread_id = Column(Integer,
                      ForeignKey('threads.id'),
                      primary_key=True,
                      unique=True)

# TODO: Include models that need to be in the database, along with their relationships
# TODO: Check how to get models metadata

