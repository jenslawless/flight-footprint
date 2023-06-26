from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import requests
from models import * 



Base = declarative_base()   
engine = create_engine('sqlite:///users_flights.db')

flight_user = Table(
    'flight_user',
    Base.metadata,
    Column('flight_id', ForeignKey('flights.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String)

    flights = relationship('Flight', secondary=flight_user, back_populates='users')


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key = True)
    
    passengers = Column(Integer)
    dep_airport = Column(String)
    des_airport = Column(String)
    carbon_g = Column(Integer)
    carbon_lb = Column(Integer)
    carbon_kg = Column(Integer)
    carbon_mt = Column(Integer)
    distance_unit = Column(String)
    distance_value = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship('User', secondary=flight_user, back_populates='flights')






