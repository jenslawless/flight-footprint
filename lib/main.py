from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import requests
from models import *
from carbon_api import *
from functions import *
from simple_term_menu import TerminalMenu
from art import *


if __name__ == '__main__':
    
    engine = create_engine('sqlite:///users_flights.db')
    # Flight.__table__.drop(engine)
    # User.__table__.drop(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

# sign user in; if no user exists, create user
    username = input('Enter your username:      ')
    find_user = session.query(User).filter(User.name == username).first()
    if find_user is None:
        print('You are not yet a registered user. Create new?')
        fetch = input('Yes or No?')
        if fetch == 'Yes' or fetch == 'yes' or fetch == 'y' or fetch =="Y":
            user = create_user(session, username)
            current_user = user

# user already exists, continue to main menu
    else: 
        user = session.query(User).filter(User.name == username).first()
        current_user = user
        print("You're logged in. Welcome to your flight footprint!")
        print(art_1)
    
    display_main_menu(session, current_user)
        


# flow of questions...
# want there to be an inital menu: add flight to database, view my flights taken, eventually...view graphs?
# after adding new flight, go back to menu...what would you like to do now? Add another flight...view all flights...
# find way to do roundtrip flights too.
# create a new user
# ask user for input for flights: no. passengers, dep and des airports
# return basic data to them
# ask if they want that data added to their overall file/graphs
# give options to view graphs of how much they have traveled