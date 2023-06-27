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

# add a new flight to user's database:
def add_flights(session, current_user):
    print(f"Great, let's add a new flight!")
    passengers = int(input('How many passengers were flying?    '))
    dep_airport = input('Where were you flying from?    ').upper()
    des_airport = input('Where were you going?    ').upper()
    fetch_flight(session, current_user, passengers, dep_airport, des_airport)
    print('Your flight was added to your database! What would you like to do now?')

# view user's info about current flights in their database
def view_database(session, current_user):
    print(f"Great, let's view your database of flights!")
    print(f"Current profile: {current_user.name}")
    print(f"Total number of flights: {len(current_user.flights)}")
    print(f"Total carbon emissions in kg: {sum(flight.carbon_kg for flight in current_user.flights)}")
    
