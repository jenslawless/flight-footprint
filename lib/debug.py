#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb

from models import *
from carbon_api import *
from functions import *
from main import *


if __name__ == '__main__':
    engine = create_engine('sqlite:///users_flights.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    print('hello')
    ipdb.set_trace()