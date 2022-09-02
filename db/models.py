from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    pass

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

# Example of the table, for the assigment refer to https://docs.sqlalchemy.org/en/14/#


class SomeTable(Base):
    __tablename__ = 'some_table'

    id = Column(Integer, primary_key=True)

# TODO: Check how to get models metadata

