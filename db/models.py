import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship
from db.connection import Base
import db.hashing

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

# TODO: Include models that need to be in the database, along with their relationships
# TODO: Check how to get models metadata

# Example of the table, for the assigment refer to https://docs.sqlalchemy.org/en/14/#
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255))
    signature = Column(String(50))
    threads = relationship("Thread")
    posts = relationship("Post")

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
    title = Column(String(255), nullable=False)
    dtCreated = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    dtUpdated = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    posts = relationship("Post")
    CheckConstraint('NOT(@dtUpdated < @dtCreated)')

    def __init__(self, id, title, dt_created, dt_updated, user_id, *args, **kwargs):
        self.id = id
        self.title = title
        self.dtCreated = dt_created
        self.dtUpdated = dt_updated
        self.user_id = user_id

class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255))
    post_id = Column(Integer, ForeignKey("posts.id"), unique=True)

    def __init__(self, id, path, post_id, *args, **kwargs):
        self.id = id
        self.path = path
        self.post_id = post_id

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String(255), nullable=True)
    dtCreated = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    dtUpdated = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    content = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    thread_id = Column(Integer, ForeignKey("threads.id"), primary_key=True, unique=True)
    attachments = relationship("Attachment")
    comments = relationship("Comment")
    CheckConstraint('CHECK(@content >= 50)')


    def __init__(self, id, title, dt_created, dt_updated, user_id, content, thread_id, *args, **kwargs):
        self.id = id
        self.title = title
        self.dtCreated = dt_created
        self.dtUpdated = dt_updated
        self.user_id = user_id
        self.content = content
        self.thread_id = thread_id

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String(255), nullable=True)
    dtCreated = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    dtUpdated = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    content = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    post_id = Column(Integer, ForeignKey('posts.id'), unique=True)

    def __init__(self, id, title, dt_created, dt_updated, content, user_id, post_id , *args, **kwargs):
        self.id = id
        self.title = title
        self.dtCreated = dt_created
        self.dtUpdated = dt_updated
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    dtCreated = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    content = Column(String(255), nullable=True)
    sender_id = Column(Integer, ForeignKey('users.id'), unique=True)
    recipient_id = Column(Integer, ForeignKey('users.id'), unique=True)

    def __init__(self, id, dt_created, content, sender_id, recipient_id, *args, **kwargs):
        self.id = id
        self.dtCreated = dt_created
        self.content = content
        self.sender_id = sender_id
        self.recipient_id = recipient_id

# class User_Thread_Link(Base):
#    __tablename__ = 'user_thread_link'
#
#    users_id = Column(Integer,
#                      ForeignKey('users.id'),
#                      primary_key=True,
#                      unique=True)
#
#    thread_id = Column(Integer,
#                       ForeignKey('threads.id'),
#                       primary_key=True,
#                       unique=True)




