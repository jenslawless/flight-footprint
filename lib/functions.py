from models import *
from carbon_api import *
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///users_flights.db')
Session = sessionmaker(bind=engine)
session = Session()


# create user
def create_user(name):
    user = User(name=f"{name}")
    session.add(user)
    session.commit()

# # fetch flight API info
# def fetch_flight(passengers, dep_airport, des_airport):
#     new_flight = Flight(passengers=f'{passengers}', dep_airport=f'{dep_airport}', des_airport=f'{des_airport}')
#     session.add(new_flight)
#     session.commit()