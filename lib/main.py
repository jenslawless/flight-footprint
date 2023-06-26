from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import requests
from models import *
from carbon_api import *
from functions import *



if __name__ == '__main__':
    
    engine = create_engine('sqlite:///users_flights.db')
    # Flight.__table__.drop(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

# sign user in; if no user exists, create user
    username = input('Enter your username: ')
    find_user = session.query(User).filter(User.name == username).first()
    if find_user is None:
        print('You are not yet a registered user. Create new?')
        fetch = input('Yes or No?')
        if fetch == 'Yes' or fetch == 'yes' or fetch == 'y':
            user = create_user(username)
            current_user = user

    else: 
        print("You're logged in. Welcome to your flight footprint!")
        user = session.query(User).filter(User.name == username).first()
        current_user = user

# add a new flight to user's database:
    add_flights = input('Do you want to add a flight to your database? Y/N')
        
    if add_flights == 'Yes' or add_flights == 'yes' or add_flights == 'y':
        passengers = input('How many passengers were flying?')
        dep_airport = input('Where were you flying from?')
        des_airport = input('Where were you going?')
        fetch_flight(current_user, passengers, dep_airport, des_airport)


            

        










# create a new user
# ask user for input for flights: no. passengers, dep and des airports

# return basic data to them

# ask if they want that data added to their overall file/graphs

# give options to view graphs of how much they have traveled

# 