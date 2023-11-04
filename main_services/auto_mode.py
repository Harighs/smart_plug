# usr/bin/python3
import sys 
sys.path.append('/home/pi/smart_plug/')
import os
from datetime import datetime, timedelta
import sqlite3
import pandas as pd

from external_services.awattar_services import AwattarServices
from database.db_manager import DatabaseManager
from pi_controller.relay_controller import RelayControl
from main_services.common_utils import common_utils 

# this service should restart every 30 minutes
class Auto_Mode:
    def __init__(self):
        self.future_df = None

    def auto_mode(self, relayNumber):
        db = DatabaseManager()
        times_toturn_on = db.read_automode_24hrs_before(relayNumber)
        if not times_toturn_on:
            return
        else:
            times_toturn_on = int(times_toturn_on[0][0])
        
        print("No of times to turn on the relay", times_toturn_on)
        self.future_df = AwattarServices().AWATTAR_FUTURE_PRICE()
        print("Data from BEFORE modification", self.future_df)

        self.date_time = datetime.now()
        print(self.date_time)

        # delete past values from future_df
        # self.future_df = self.future_df[self.future_df['start_timestamp'] >= self.date_time.now()]

        # find min 2 values of future_df
        self.future_df.sort_values(by=['marketprice'], inplace=True)
        self.future_df = self.future_df.iloc[:times_toturn_on]
        self.future_df.sort_values(by=['start_timestamp'], inplace=True)
        # add extra columns to data frame and to match database table "automaterelay"
        self.future_df['triggerstatus'] = True
        self.future_df['unit'] = "kWh"
        self.future_df['relaynumber'] = relayNumber

        print("Data from AFTER modification", self.future_df)

        if len(self.future_df) > 0:
            print("Found matching auto mode for relay:", relayNumber)
            conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")
            self.future_df.to_sql('automaterelay', conn, index=False, if_exists='append') # replace the dataset
            self.future_df.to_sql('automaterelay_report', conn, index=False, if_exists='append') # for report purpose
            conn.close()
        else:
            print("No matching auto mode")

        self.turn_on_turn_off(relayNumber)

    
    def delete_automate_relay(self):
            conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")
            cursor = conn.cursor()
            delete_query = "DELETE from automaterelay"
            cursor.execute(delete_query)
            conn.commit()
            conn.close()



    def turn_on_turn_off(self, relayNumber):
        # check whether the relay 1 or 2 is on Auto mode then turn on and turn off automatically
        db = DatabaseManager()
        results = db.read_relaymode_temp(relayNumber) # setting relay number
                
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime('%Y-%m-%dT%H:00:00')

        buffer_datetime = datetime.now() + timedelta(hours=1)
        buffer_datetime = buffer_datetime.strftime('%Y-%m-%dT%H:00:00')

        conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")
        query = f"SELECT * from automaterelay where relaynumber={relayNumber} and start_timestamp BETWEEN '{current_datetime}' and '{buffer_datetime}'"
        new_dataframe = pd.read_sql_query(query, conn)

        print(query)
        print(new_dataframe)


        if len(results) > 0: # check whether relay is on Auto Mode
                # check if new_dataframe is empty then turn off the relay
                if(new_dataframe.empty):
                     # Turn OFF
                    RelayControl().relayController(relayNumber, 0)
                    print(f"Relay {relayNumber} turned off in AutoMode")

                current_time = datetime.now()
                # Check if current time is within any interval
                for index, row in new_dataframe.iterrows():
                    startdatetime = pd.to_datetime(row['start_timestamp'])
                    enddatetime = pd.to_datetime(row['end_timestamp'])
                    print("startdatetime", startdatetime)
                    print("enddatetime", enddatetime)
                    print("current_time", current_time)

                    if startdatetime <= current_time <= enddatetime:
                        # Turn On
                        RelayControl().relayController(relayNumber, 1)
                        print(f"Relay {relayNumber} turned on in AutoMode")
                        break
                    else:
                        # Turn OFF
                        RelayControl().relayController(relayNumber, 0)
                        print(f"Relay {relayNumber} turned off in AutoMode")

if __name__ == "__main__":
    auto_mode = Auto_Mode()
    auto_mode.delete_automate_relay()
    
    auto_mode.auto_mode(1)
    auto_mode.auto_mode(2)
