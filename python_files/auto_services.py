"""
In this file we have to call both services and store the datasets to the local
sqlite database

TODO 1: get those two methods from api_services.py (see TODO 5)
TODO 2: call the awattar and smart meter services 
TODO 3: store the information to the database table (datacache) and use db_manager().insert(?, ?, ?, ?)
"""

import os
import schedule
import pandas as pd
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

def create_master_df(awattar_data_path, smart_meter_data_path):
    Master_Data_Path = '../DATASET/master_data.csv'
    
    if not os.path.exists(Master_Data_Path):
        columns  = ['start_timestamp', 'end_timestamp', 'awattar_price', 'smart_meter_consumption', 'R1', 'R2', 'R3', 'R4', 'R5', 'status','mode']
        pd.DataFrame(columns=columns).to_csv(Master_Data_Path, index=False)
    
    Master_Data = pd.read_csv(Master_Data_Path)
    
    # Load and process awattar data
    awattar_data = pd.read_csv(awattar_data_path)
    
    # Load and process smart meter data
    smart_meter_data = pd.read_csv(smart_meter_data_path)
    
    smart_meter_data['peakDemandTimes'] = pd.to_datetime(smart_meter_data['peakDemandTimes'])
    smart_meter_data['hourly_time'] = smart_meter_data['peakDemandTimes'].dt.floor('H')
    smart_meter_data = smart_meter_data.groupby('hourly_time')['meteredValues'].sum().reset_index()
    
        
    Master_Data['start_timestamp'] = awattar_data['start_timestamp']
    Master_Data['end_timestamp'] = awattar_data['end_timestamp']
    Master_Data['awattar_price'] = awattar_data['marketprice']
    Master_Data['smart_meter_consumption'] = smart_meter_data['meteredValues']
    # R1
    Master_Data['R1'] = smart_meter_data['meteredValues']
    # R4
    Master_Data['R4'] = awattar_data['marketprice']
    # R2
    Master_Data['R2'] = Master_Data['R1'] * Master_Data['R4']  # R2 = R1 * R4
    # R5
    Master_Data['R5'] = Master_Data['R2'] - Master_Data['R1'] * Master_Data['R4']  # R5 = (R2 - R1) * R4
    
    # R3
    Master_Data[['R1', 'R2']].replace(0, 0.0001, inplace=True)
    Master_Data[['R1' , 'R2']].fillna(0.0001, inplace=True)
    Master_Data['R3'] = Master_Data['R2'] / Master_Data['R1']  # R3 = R2 / R1

    # fill NaN on chosen columns with 0
    Master_Data[['R1', 'R2', 'R3', 'R4', 'R5']] = Master_Data[['R1', 'R2', 'R3', 'R4', 'R5']].fillna(0)
    
    Master_Data.to_csv(Master_Data_Path, index=False)

    return True
    
    