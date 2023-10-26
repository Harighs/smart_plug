# usr/bin/python3
import sys 
sys.path.append('/home/pi/smart_plug/')

import datetime
import sqlite3

from external_services.awattar_services import AwattarServices
from database.db_manager import DatabaseManager

# Add the directory to sys.path
sys.path.append('..')
from pi_controller.relay_controller import RelayControl
from main_services.common_utils import common_utils 

# this service should restart every 30 minutes


class Auto_Mode:
    def __init__(self):
        self.future_df = None
        pass

    def auto_mode(self):
        db = DatabaseManager()
        times_toturn_on = db.read_automode_24hrs_before(1) # relay1
        times_toturn_on = int(times_toturn_on[0][0])

        self.future_df = AwattarServices().AWATTAR_FUTURE_PRICE()

        self.date_time = datetime.datetime.now()
        # delete past values from future_df
        self.future_df = self.future_df[self.future_df['start_timestamp'] > self.date_time.now()]

        # find min 2 values of future_df
        self.future_df.sort_values(by=['marketprice'], inplace=True)
        self.future_df = self.future_df.iloc[:times_toturn_on]
        self.future_df.sort_values(by=['start_timestamp'], inplace=True)
        # add extra columns to data frame and to match database table "automaterelay"
        self.future_df['triggerstatus'] = True
        self.future_df['unit'] = "kWh"
        self.future_df['relaynumber'] = 1 #relay1

        print(self.future_df)

        if len(self.future_df) > 0:
            print("Found matching auto mode")
             # Feed Master Data CSV to the database
            conn = sqlite3.connect("database/"+common_utils.static_database_filename)
            self.future_df.to_sql('automaterelay', conn, index=False, if_exists='append')
        else:
            print("No matching auto mode")


        return self.future_df

    def turn_on_turn_off(self):
        # TODO: get DB data and change to dataframe
        # check whether the relay 1 or 2 is on Auto mode then turn on and turn off automatically

        current_time = datetime.datetime.now()
        # Check if current time is within any interval
        while True:
            for index, row in self.future_df.iterrows():
                if not row['start_timestamp'] <= current_time <= row['end_timestamp']:
                    # Turn On
                    RelayControl().relayController(relayNumber=1, relayStatus=1)
                else:
                    # Turn OFF
                    RelayControl().relayController(relayNumber=1, relayStatus=0)


if __name__ == "__main__":
    auto_mode = Auto_Mode()
    auto_mode.auto_mode()
    #auto_mode.turn_on_turn_off()
    #print(auto_mode.future_df)
