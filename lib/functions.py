from models import *
from carbon_api import *
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from simple_term_menu import TerminalMenu


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

# delete a flight
def delete_flights(session, current_user):
    print("Which flight do you want to delete?")
    flight_options = [f"Flight from {flight.dep_airport} to {flight.des_airport} ({flight.passengers} passengers on this flight)"
                      for flight in current_user.flights  
    ]
    terminal_menu = TerminalMenu(flight_options)
    menu_entry_index = terminal_menu.show()
    
    if menu_entry_index >= 0 and menu_entry_index < len(current_user.flights):
        selected_flight = current_user.flights[menu_entry_index]
        associated_users = session.query(User).filter(User.flights.any(id == selected_flight.id)).all()
        
        # checks if the flight is only associated with this user. If so, deletes the flight instance entirely
        if len(associated_users) == 1:
            current_user.flights.remove(selected_flight)
            session.delete(selected_flight)

        # else, we only remove the association between the user and this flight. The flight remains associated with other users.
        else:
            current_user.flights.remove(selected_flight)

        session.commit()
        print("Flight successfully deleted!")
    else:
        print("Invalid selection")
    

    
# update a flight
def update_flight(session, current_user):
    print("updating flights!")
    
