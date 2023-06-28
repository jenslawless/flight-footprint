import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import * 



# use user's inputs to fetch carbon emissions info from API:
def fetch_flight(session, current_user, passengers, dep_airport, des_airport):
    
  existing_flight = session.query(Flight).filter(
        Flight.passengers == passengers,
        Flight.dep_airport == dep_airport,
        Flight.des_airport == des_airport
  ).first()
    
  if existing_flight is not None:
        # Flight already exists, associate it with the current user
        current_user.flights.append(existing_flight)
        session.commit()

  else:
        headers = dict([
          ("Content-Type",  "application/json"),
          ("Authorization", "Bearer aiPLtFvh7zQoAJogPyw4Q")
        ])

        body = {
              "type": "flight",
              "passengers": passengers,
              "legs": [
                {"departure_airport": dep_airport, "destination_airport": des_airport},
              ],
              "distance_unit": "km"
            }
            
        new_flight = requests.post('https://www.carboninterface.com/api/v1/estimates', json=body, headers=headers).json()
        
        passengers = new_flight['data']['attributes']['passengers']
        dep_airport = new_flight['data']['attributes']['legs'][0]['departure_airport']
        des_airport = new_flight['data']['attributes']['legs'][0]['destination_airport']
        carbon_g = new_flight['data']['attributes']['carbon_g']
        carbon_lb = new_flight['data']['attributes']['carbon_lb']
        carbon_kg = new_flight['data']['attributes']['carbon_kg']
        carbon_mt = new_flight['data']['attributes']['carbon_mt']
        distance_unit = new_flight['data']['attributes']['distance_unit']
        distance_value = new_flight['data']['attributes']['distance_value']
      
        new_flight_entry = Flight(
            user_id = current_user.id,
            passengers=passengers, 
            dep_airport=dep_airport, 
            des_airport=des_airport, 
            carbon_g=carbon_g,
            carbon_lb=carbon_lb, 
            carbon_kg=carbon_kg, 
            carbon_mt=carbon_mt, 
            distance_unit=distance_unit,
            distance_value=distance_value)

        session.add(new_flight_entry)
        current_user.flights.append(new_flight_entry)
        session.commit()



      

    
    














# # format of data retrieved

# # {'data':
# #   {'id': '2c2aeca0-076d-4eac-afc5-b36faf0334ee',
# #    'type': 'estimate',
# #    'attributes':
# #       {'passengers': 3,
# #        'legs':
# #               [{'departure_airport': 'ORD', 'destination_airport': 'LHR'},
# #                {'departure_airport': 'LHR', 'destination_airport': 'ORD'}],
# #        'distance_value': 12928.9,
# #        'distance_unit': 'km',
# #        'estimated_at': '2023-06-26T16:36:26.105Z',
# #        'carbon_g': 4406724,
# #        'carbon_lb': 9715.16,
# #        'carbon_kg': 4406.72,
# #        'carbon_mt': 4.41
# #        }
# #   }
# # }
 