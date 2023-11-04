"""
In this file we have to call both services and store the datasets to the local
sqlite database
"""

import sys 
sys.path.append('/home/pi/smart_plug/')
import os
import pandas as pd
import sqlite3

from external_services.awattar_services import AwattarServices
from external_services.smartmeter_services import SmartMeterServices
from database.db_manager import DatabaseManager
from main_services.common_utils import common_utils 

import time
from datetime import datetime
import timedelta

current_dir = os.getcwd()
print("Current working directory:", current_dir)

class AutoServices:
    def __init__(self):
        awattar_services = AwattarServices()
        smartmeter_services = SmartMeterServices()

        self.awattar_df = awattar_services.AWATTAR_ONE_DAY_PERIOD()
        self.smartmeter_df = smartmeter_services.sm_each_date()

        self.awattar_data_path = '/home/pi/smart_plug/dataset/'+common_utils.static_awattar_filename
        self.smart_meter_data_path = '/home/pi/smart_plug/dataset/'+common_utils.static_smartmeter_filename

    def create_master_df(self):
        Master_Data_Path = '/home/pi/smart_plug/dataset/'+common_utils.static_master_service

        if not os.path.exists(Master_Data_Path):
            columns = ['start_timestamp', 'end_timestamp', 'awattar_price', 'smart_meter_consumption', 'R1', 'R2', 'R3',
                       'R4', 'R5', 'status', 'mode']
            pd.DataFrame(columns=columns).to_csv(Master_Data_Path, index=False)

        Master_Data = pd.read_csv(Master_Data_Path)

        # Load and process awattar data
        awattar_data = pd.read_csv(self.awattar_data_path)

        # Load and process smart meter data
        smart_meter_data = pd.read_csv(self.smart_meter_data_path)

        smart_meter_data['peakDemandTimes'] = pd.to_datetime(smart_meter_data['peakDemandTimes'])
        smart_meter_data['hourly_time'] = smart_meter_data['peakDemandTimes'].dt.floor('H')
        smart_meter_data = smart_meter_data.groupby('hourly_time')['meteredValues'].sum().reset_index()

        Master_Data['start_timestamp'] = awattar_data['start_timestamp']
        Master_Data['end_timestamp'] = awattar_data['end_timestamp']
        Master_Data['awattar_price'] = awattar_data['marketprice'] / 1000  # Converting mWh to kWh
        Master_Data['smart_meter_consumption'] = smart_meter_data['meteredValues']
        Master_Data['awattar_unit'] = awattar_data['unit']
        Master_Data['smart_meter_unit'] = "kWh"
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
        Master_Data[['R1', 'R2']].fillna(0.0001, inplace=True)
        Master_Data['R3'] = Master_Data['R2'] / Master_Data['R1']  # R3 = R2 / R1

        # fill NaN on chosen columns with 0
        Master_Data[['R1', 'R2', 'R3', 'R4', 'R5']] = Master_Data[['R1', 'R2', 'R3', 'R4', 'R5']].fillna(0)

        if os.path.exists(Master_Data_Path):
            os.remove(Master_Data_Path) 
        Master_Data.to_csv(Master_Data_Path, index=False)

        # Feed Master Data CSV to the database
        conn = sqlite3.connect("/home/pi/smart_plug/database/"+common_utils.static_database_filename)
        # Reset the index to use auto-incrementing values
        Master_Data.reset_index(drop=True, inplace=True)
        Master_Data.to_sql('datacache', conn, if_exists='replace', index_label='id')

        Master_Data.reset_index(drop=True, inplace=True)
        Master_Data.to_sql('datacache_report', conn, if_exists='append', index_label='id')
        
        return True
    
    def calculateAutoModeValue(self, relayNumber):
        db = DatabaseManager()

        if(relayNumber == 1):
            relayPower = db.read_relaysettings_table()[0][2] # relay 1 power
        elif(relayNumber == 2):
            relayPower = db.read_relaysettings_table()[0][3] # relay 2 power
        
        last_known_times_toturn_on = db.read_automode_24hrs_before(relayNumber)
        last_known_times_toturn_on = int(last_known_times_toturn_on[0][0]) * int(relayPower)
        last_24hrs_usage = db.read_datacache_last_24hrs_consumption()[0][0] # A
        
        """
        Formula to calculate auto_mode value
        A = Last 24hrs consumption
        B = Power needed for Relay1 or Relay 2
        Result = A/B

        Example: A = 20KW; B = 5KW
            Result = 20/5 
                   = 4 times (this we have to turn on and turn off the relay automatically)

        Escalation Example:
            Lets say times_turnon=6*Relay power (20kwh)
                E old = 6*20 = 120 kwh 
            If the last 24hrs consumption is greater or equal to (E Old) then multiply with escalation value
        """
      
        # Logic for Escalation --> 1.3 default value
        # Higher the demand higher the turn on time
        if(last_known_times_toturn_on >= last_24hrs_usage):
            no_of_times_to_activate_automode = last_24hrs_usage * 1.3 / int(relayPower)
            db.insert_automode(last_24hrs_usage, relayNumber, round(no_of_times_to_activate_automode)) 
        else:
            no_of_times_to_activate_automode = int(last_24hrs_usage) / int(relayPower)
            db.insert_automode(last_24hrs_usage, relayNumber, round(no_of_times_to_activate_automode)) 

        return True



if __name__ == '__main__':
    auto_service = AutoServices()
    auto_service.create_master_df()
    auto_service.calculateAutoModeValue(1)
    auto_service.calculateAutoModeValue(2)


