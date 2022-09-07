from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, Table
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship
from db.connection import Base
from db.thread.models import Thread

@as_declarative()
class Base:
    pass

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

# Example of the table, for the assigment refer to https://docs.sqlalchemy.org/en/14/#
class Post(Thread):
    __tablename__ = 'post'

    __mapper_args__ = {
        "polymorphic_identity": "post",
    }
    id = Column(Integer, ForeignKey("thread.id"), primary_key=True)
    content = Column(String(255))
    CheckConstraint('CHECK(@content >= 30)')
    files = relationship("File")

    def __init__(self, id, title, dt_created, dt_updated, user_id, content, *args, **kwargs):
        super().__init__(id,title,dt_created,dt_updated,user_id)
        self.content = content

class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255))
    thread_id = Column(Integer, ForeignKey("thread.id"))

    def __init__(self, id, path, *args, **kwargs):
        self.id = id
        self.path = path

# TODO: Include models that need to be in the database, along with their relationships
# TODO: Check how to get models metadata

