# Phase 3 CLI Project -- Flight Footprint

## Overview

- Flight Footprint allows users to input data for a flight they already took or are planning to take (# of passengers, departure airport, and destination airport) and receive back the carbon emissions generated from their trip.
- All of a user's flights are stored in a database associated with them as a user.
- Graphs are accessible to compare a user's carbon emissions to others and also compare their own flights to each other 

---

## How to Download

- Fork and clone this repo
- Install the pip file via the commands below

```sh
pipenv install && pipenv shell
pip install simple-term-menu
pip install SQLAlchemy
pipenv install sqlalchemy alembic
```

---

## File Tree

```sh
.
├── alembic.ini
├── art.py
├── carbon_api.py
├── debug.py
├── functions.py
├── main.py
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── models.py
└── users_flights.db
```

The structure for Flight Footprint is above. Below are the functions for each file.
- 'art.py' contains the intro artwork that reads  "Flight Footprint"
- 'carbon_api.py' contains the fetch request to the Carbon Interface API. This is where the    "fetch_flight" function lives and every time a new flight is created, this function is accessed.
    - Documentation and more information about the Fetch request can be found at the Carbon Interface website: https://docs.carboninterface.com/#/?id=flight

- 'functions.py' contains all other functions for this app including: 
    - creating a user: creates a new instance of the User class and commits it to the database
    - deleting a flight: checks to see if other users are also associated with the flight instance the current_user is trying to delete. If they are, the flight association is just removed between the current_user and the selected flight. If there is no other user associated with the flight, the flight instance is deleted.
    - updating a flight: users can updated a flight they already input by updating the number of passengers, the departure airport or the destination airport. If the flight is associated with other users, a new flight instance is created so they other users flight is not also updated.
    - Graphs:
        - There are a few graphs users can view:
            - Compare their emissions to the average users total emissions (calculated by removing the current_users emissions, totaling and dividing by the rest of the users)
            - Compare the flights this user is taking. The numbers showed are per passenger. So if a user has a flight that has 5 passengers and a flight for 2 passengers, the bar graph shown will show the amount of carbon emissions per passenger for each of those flights.
    - Menus:
        - There is a main menu and a sub-menu for the graphs. These were generated using simple-term-menu
- 'main.py' is the script for this app. More info on this below.
- 'models.py' contains the models for the tables: 
    - User: creates an instance of the User class, just with a name and id.
    - Flight: this takes in the number of passengers, departure airport and destination airport. Once the fetch is posted, it gets back all the calculations of carbon emissions and creates the new flight isntance.
    - Flight_user: the association table between users and flights.  
- 'user_flights.db' is the database that contains the data created from the app

---

### Running the app

To run the app, cd into the lib folder and run the main file (demonstrated below)

```sh
cd lib
python main.py
```

Enter a new username. Then you can add a flight, update an existing flight, delete a flight or view graphs to offer insights. 

---
