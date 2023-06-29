from models import *
from carbon_api import *
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from simple_term_menu import TerminalMenu
import time
import matplotlib.pyplot as plt
import pandas as pd


# create user
def create_user(session, name):
    user = User(name=name)
    session.add(user)
    session.commit()
    return user

# add a new flight to user's database:
def add_flights(session, current_user):
    print(f"Great, let's add a new flight!")
    passengers = int(input('How many passengers were flying?    '))
    dep_airport = input('Where were you flying from?    ').upper()
    des_airport = input('Where were you going?    ').upper()
    fetch_flight(session, current_user, passengers, dep_airport, des_airport)
    print('Your flight was added to your database!')
    time.sleep(1)
    display_main_menu(session, current_user)

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
    
    time.sleep(1)
    display_main_menu(session, current_user)


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
        elif selected_item_to_update == "destination airport":
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
    time.sleep(1)
    display_main_menu(session, current_user)

def exit_out(session):
    session.close()

def display_main_menu(session, current_user):
    print("What would you like to do?")

    options = ["Add a new flight", "Delete a flight", "Update an existing flight", "Show me a graph", "Exit out of Flight Footprint"]
    option_actions = [
        lambda: add_flights(session, current_user),
        lambda: delete_flights(session, current_user),
        lambda: update_flight(session, current_user),
        lambda: graphs_menu(session, current_user),
        lambda: exit_out(session)
        ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    option_actions[menu_entry_index]()


# shows bar chart of the user's flight and how much emissions are generated
def graph_1(session, current_user):
    user_flights = session.query(Flight).join(Flight.users).filter(User.id == current_user.id).all()

    flight_details = [
    {'departure_airport': flight.dep_airport, 'destination_airport': flight.des_airport}
    for flight in user_flights
    ]
    passenger_counts = [flight.passengers for flight in user_flights]
    emissions = [flight.carbon_kg for flight in user_flights]

    fig, ax = plt.subplots()
    bars = ax.bar(range(len(emissions)), emissions)
    plt.xticks(range(len(emissions)), [f"{flight['departure_airport']} to {flight['destination_airport']}" for flight in flight_details])
    ax.set_ylabel('Carbon Emissions (kg)')

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f"{passenger_counts[i]} passengers", ha='center', va='bottom')

    plt.show()
    graphs_menu(session, current_user)

# graph shows the current_users total carbon emissions/kg compared to the average user (average of the totals of all users)
def graph_2(session, current_user):
     total_emissions = session.query(
        User.id, 
        User.name, 
        func.sum(Flight.carbon_kg).label('total_emissions')
     ).join(flight_user, User.id == flight_user.c.user_id).join(Flight, Flight.id == flight_user.c.flight_id).group_by(User.id).all()
    
     df = pd.DataFrame(total_emissions, columns=['user_id', 'user_name', 'total_emissions'])
     current_user_total = df.loc[df['user_id'] == current_user.id]['total_emissions'].iloc[0] 
     average_total = df['total_emissions'].mean()

     fig, ax = plt.subplots()
     ax.bar(['Current User', 'Average Total for Other Users'], [current_user_total, average_total])
     ax.set_ylabel('Total Carbon Emissions (kg)')

     plt.show()
     graphs_menu(session, current_user)

# menu for graphs
def graphs_menu(session, current_user):
     print("Which graph would you like to view?")

     options = ["My total emissions compared to average user", "My flights compared to each other", "My database of flights", "Back to main menu",]
     option_actions = [
        lambda: graph_2(session, current_user),
        lambda: graph_1(session, current_user),
        lambda: user_database(session, current_user),
        lambda: display_main_menu(session, current_user)
        ]
     terminal_menu = TerminalMenu(options)
     menu_entry_index = terminal_menu.show()
     option_actions[menu_entry_index]()
     display_main_menu(session, current_user)

def user_database(session, current_user):
    user_database = session.query(
        User.id,
        Flight.passengers,
        Flight.dep_airport,
        Flight.des_airport,
        Flight.carbon_g,
        Flight.carbon_lb, 
        Flight.carbon_kg, 
        Flight.carbon_mt,
        Flight.distance_value,
        Flight.distance_unit
    ).join(flight_user, User.id == flight_user.c.user_id).join(Flight, Flight.id == flight_user.c.flight_id).filter(User.id == current_user.id).all()

    df = pd.DataFrame(user_database, columns=['user_id', 'no_passengers', 'dep_airport', 'des_airport', 'carbon_g', 'carbon_lb', 'carbon_kg', 'carbon_mt', 'distance_value', 'distance_unit'])
    df = df.drop('user_id', axis=1)
    df = df.reset_index(drop=True)

    average_flight = df['carbon_kg'].mean()
    time.sleep(1)
    print(f'The average carbon emissions in kg you are generating each flight is: {average_flight}')
    time.sleep(1)
    print(df)
    time.sleep(2)
    graphs_menu(session, current_user)



 




    


    

    
   

 



    
