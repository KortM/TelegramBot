import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

basedir =os.path.abspath(os.path.dirname(__file__))
name = '/BD.db'
engine = create_engine("sqlite:///"+basedir+name)
print(basedir+name)
Base = declarative_base()
Session =sessionmaker(bind= engine)
class Mac(Base):
    __tablename__ = 'Mac'
    id = Column(Integer, primary_key=True)
    A = Column(String(10))
    B = Column(String(10))
    C = Column(String(10))
    title = Column(String(30))
    address = Column(String(30))

    def __init__(self,A,B,C, title, address):
        self.A = A
        self.B = B
        self.C = C
        self.title = title
        self.address = address
    def __repr__(self):
        return("{0}:{1}:{2}".format(self.A, self.B, self.C))
class Country(Base):
    __tablename__ = 'Country'
    id = Column(Integer, primary_key=True)
    code = Column(String(2))
    title = Column(String(20))

    def __init__(self, code, title):
        self.code = code
        self.title = title

    def __repr__(self):
        return "{0}:{1}".format(self.code, self.title)

class RussianNubmers(Base):
    __tablename__ = 'RussianNumbers'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    start_number = Column(String(20))
    end_number = Column(String(20))
    cap = Column(String(20))
    operator = Column(String(20))
    region = Column(String(50))

    def __init__(self, code, start_number, end_number, cap, operator, region):
        self.code = code
        self.start_number = start_number
        self.end_number = end_number
        self.cap = cap
        self.operator = operator
        self.region = region

    def __repr__(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}".format(self.code, self.start_number, self.end_number, self.cap, self.operator, self.region)

class CountryCode(Base):
    __tablename__ = 'CountryCode'
    id = Column(Integer, primary_key=True)
    country = Column(String(30))
    code = Column(Integer)
    def __init__(self, country, code):
        self.country = country
        self.code = code
    def __repr__(self):
        return "{0}, {1}".format(self.country, self.code)

Base.metadata.create_all(engine)