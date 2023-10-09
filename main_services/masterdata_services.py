"""
In this file we have to call both services and store the datasets to the local
sqlite database

TODO 1: get those two methods from api_services.py (see TODO 5)
TODO 2: call the awattar and smart meter services 
TODO 3: store the information to the database table (datacache) and use db_manager().insert(?, ?, ?, ?)
"""

import sys 
sys.path.append('/home/pi/smart_plug')
import os
import pandas as pd
import sqlite3

from external_services.awattar_services import AwattarServices
from external_services.smartmeter_services import SmartMeterServices


class AutoServices:
    def __init__(self):
        awattar_services = AwattarServices()
        smartmeter_services = SmartMeterServices()

        self.awattar_df = awattar_services.AWATTAR_ONE_DAY_PERIOD()
        self.smartmeter_df = smartmeter_services.sm_each_date()

        self.awattar_data_path = '../dataset/awattar_data.csv'
        self.smart_meter_data_path = '../dataset/smart_meter_data.csv'

    def create_master_df(self):
        Master_Data_Path = '../dataset/master_data.csv'

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
        conn = sqlite3.connect("../database/pythonsqlite.db")
        Master_Data.to_sql('datacache', conn, index=False, if_exists='append')
        return True


if __name__ == '__main__':
    auto_service = AutoServices()
    auto_service.create_master_df()
