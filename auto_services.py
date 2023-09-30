"""
In this file we have to call both services and store the datasets to the local
sqlite database

TODO 1: get those two methods from api_services.py (see TODO 5)
TODO 2: call the awattar and smart meter services 
TODO 3: store the information to the database table (datacache) and use db_manager().insert(?, ?, ?, ?)
"""

import os
import schedule
import time

from flask import Flask, jsonify, request

from external_services.awattar_services import AwattarServices
from pi_controller.relay_controller import RelayControl
from external_services.smartmeter_services import SmartMeterServices



# Get R1 and R4 values
smartmeter_data = SmartMeterServices()
# R1 = smartmeter_data.getConsolidatedData(fromDate_sm, toDate_sm)  ## str: value old method
fromDate_sm = '2023-09-30 00:15:00'
toDate_sm = '2023-09-01 00:00:00'
# R1 = smartmeter_data.get_smart_meter_data(fromDate_sm, toDate_sm)  ## str: value


get_avg_data = AwattarServices()
R4 = get_avg_data.get_average_awattar_price_over_period(fromDate_sm, toDate_sm)

print(R4)