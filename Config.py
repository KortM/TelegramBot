import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#basedir =os.path.abspath(os.path.dirname(__file__))
name = 'BD.db'
engine = create_engine("sqlite:///"+name, connect_args={'check_same_thread': False})
Base = declarative_base()
Session =sessionmaker(bind= engine)

class InternationTelephonyCodes(Base):
    __tablename__ = 'Country'
    id = Column(Integer, primary_key=True)
    code = Column(String(2))
    title = Column(String(20))

    def __init__(self, code, title):
        self.code = code
        self.title = title

    def __repr__(self):
        return "{0}:{1}".format(self.code, self.title)

class CodesOfCountry(Base):
    __tablename__ = 'CountryCode'
    id = Column(Integer, primary_key=True)
    country = Column(String(30))
    title = Column(String(150))
    def __init__(self, country, title):
        self.country = country
        self.title = title
    def __repr__(self):
        return "{0}, {1}".format(self.country, self.title)

Base.metadata.create_all(engine)