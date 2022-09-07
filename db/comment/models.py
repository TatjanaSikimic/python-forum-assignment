from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship
from db.connection import Base

@as_declarative()
class Base:
    pass

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

# Example of the table, for the assigment refer to https://docs.sqlalchemy.org/en/14/#
class Comment(Base):
    __tablename__ = 'comments'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    # title = Column(String)


# TODO: Include models that need to be in the database, along with their relationships
# TODO: Check how to get models metadata

