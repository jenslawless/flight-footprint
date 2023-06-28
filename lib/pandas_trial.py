import pandas as pd

df = pd.read_csv('sqlite:///users_flights.db')

print(df.head())