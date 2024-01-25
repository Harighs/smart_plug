"""
This is the fallback services to retrieve the master data set
This check whether "automode" is already data available 
"""

import sys 
sys.path.append('/home/pi/smart_plug/')
import os
import pandas as pd
import sqlite3
import math

from external_services.awattar_services import AwattarServices
from external_services.smartmeter_services import SmartMeterServices

from main_services.masterdata_services import AutoServices

from database.db_manager import DatabaseManager
from main_services.auto_mode import Auto_Mode
from main_services.common_utils import common_utils 

import time
from datetime import datetime
import timedelta

current_dir = os.getcwd()
print("Current working directory:", current_dir)

class FallbackServices:
    def __init__(self):
        db = DatabaseManager()
        result = db.check_automode_table()
        print(result[0])
        result0 = result[0]
        if(result0 == 0): # Data download not yet done then run the masterdata service
                auto_service = AutoServices()
                # Delete the master csv before creation
                Master_Data_Path = '/home/pi/smart_plug/dataset/'+common_utils.static_master_service
                if os.path.exists(Master_Data_Path):
                    os.remove(Master_Data_Path)
                auto_service.create_master_df()
                auto_service.calculateAutoModeValue(1)
                auto_service.calculateAutoModeValue(2)
                print("Fallback call initiated...")
        else:
                print("Fallback is not necessary today! Data already downloaded...")
            
        return

if __name__ == '__main__':
    fallbackServices = FallbackServices()
