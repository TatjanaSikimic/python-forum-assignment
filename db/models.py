import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship
from db.connection import Base
import db.hashing

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
        self.password = db.hashing.get_password_hash(password)
        self.avatar = avatar
        self.signature = signature

    def check_password(self, password):
        return db.hashing.verify_password(self.password, password)

# class Thread(Base):
#     __tablename__ = 'threads'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String(255))
#     dtCreated = Column(DateTime, default=datetime.datetime.utcnow)
#     # dodati neko ogranicenje da datum updejtovanja ne bude manji od datuma kreiranja?
#     dtUpdated = Column(DateTime, default=datetime.datetime.utcnow)
#     # CheckConstraint('NOT(@dtUpdated < @dtCreated)')
#     user_id = Column(Integer, ForeignKey("user.id"))
#
#     __mapper_args__ = {
#         "polymorphic_identity": "thread",
#         "polymorphic_on": type,
#     }
#
#     def __init__(self, id, title, dt_created, dt_updated, user_id, *args, **kwargs):
#         self.id = id
#         self.title = title
#         self.dtCreated = dt_created
#         self.dtUpdated = dt_updated
#         self.user_id = user_id

# class Post(Thread):
#     __tablename__ = 'post'
#
#     __mapper_args__ = {
#         "polymorphic_identity": "post",
#     }
#     id = Column(Integer, ForeignKey("thread.id"), primary_key=True)
#     content = Column(String(255))
#     CheckConstraint('CHECK(@content >= 30)')
#     files = relationship("File")
#
#     def __init__(self, id, title, dt_created, dt_updated, user_id, content, *args, **kwargs):
#         super().__init__(id,title,dt_created,dt_updated,user_id)
#         self.content = content
#
# class File(Base):
#     __tablename__ = 'file'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     path = Column(String(255))
#     thread_id = Column(Integer, ForeignKey("thread.id"))
#
#     def __init__(self, id, path, *args, **kwargs):
#         self.id = id
#         self.path = path

# class Comment(Base):
    __tablename__ = 'comments'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    # title = Column(String)
# TODO: Include models that need to be in the database, along with their relationships
# TODO: Check how to get models metadata

