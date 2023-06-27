from models import *
from carbon_api import *
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from simple_term_menu import TerminalMenu
import time


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
    time.sleep(4)


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
    print("Which flight do you want to update?")
    flight_options = [f"Flight from {flight.dep_airport} to {flight.des_airport} ({flight.passengers} passengers on this flight)"
                      for flight in current_user.flights  
    ]
    terminal_menu = TerminalMenu(flight_options)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index >= 0 and menu_entry_index < len(current_user.flights):

        selected_flight = current_user.flights[menu_entry_index]

        print("Which part of this flight would you like to update?")
        update_options = ["number of passengers", "departure airport", "destination airport"]
        terminal_menu = TerminalMenu(update_options)
        menu_entry_index = terminal_menu.show()
        selected_item_to_update = update_options[menu_entry_index]
        
        # update number of passengers:
        if selected_item_to_update == "number of passengers":
            new_passengers = int(input("Enter the updated number of passengers:   "))
            
            existing_flight = session.query(Flight).filter(
                Flight.passengers == new_passengers,
                Flight.dep_airport == selected_flight.dep_airport,
                Flight.des_airport == selected_flight.des_airport
            ).first()

            if existing_flight is not None:
                current_user.flights.append(existing_flight)
            else: 
                fetch_flight(session, current_user, new_passengers, selected_flight.dep_airport, selected_flight.des_airport)


        # update departure airport
        elif selected_item_to_update == "departure airport":
            new_dep_airport = input("Enter the new departure airport:  ").upper()

            existing_flight = session.query(Flight).filter(
                Flight.passengers == selected_flight.passengers,
                Flight.dep_airport == new_dep_airport,
                Flight.des_airport == selected_flight.des_airport
            ).first()

            if existing_flight is not None:
                current_user.flights.append(existing_flight)
            else: 
                fetch_flight(session, current_user, selected_flight.passengers, new_dep_airport, selected_flight.des_airport)

        # updated destination airport
        elif selected_item_to_update == "destination airport:":
            new_des_airport = input("Enter the new destination airport:   ").upper()
            existing_flight = session.query(Flight).filter(
                Flight.passengers == selected_flight.passengers,
                Flight.dep_airport == selected_flight.dep_airport,
                Flight.des_airport == new_des_airport
            ).first()

            if existing_flight is not None:
                current_user.flights.append(existing_flight)
            else: 
                fetch_flight(session, current_user, selected_flight.passengers, selected_flight.dep_airport, new_des_airport)        
    
    current_user.flights.remove(selected_flight)
    session.commit()

def exit_out(session):
    session.close()

    
