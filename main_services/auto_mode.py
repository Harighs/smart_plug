# usr/bin/python3
import sys 
sys.path.append('/home/pi/smart_plug/')

import datetime

from external_services.awattar_services import AwattarServices

# Add the directory to sys.path
sys.path.append('..')
from pi_controller.relay_controller import RelayControl


class Auto_Mode:
    def __init__(self):
        self.future_df = None
        pass

    def auto_mode(self, no_of_times: int):
        self.future_df = AwattarServices().AWATTAR_FUTURE_PRICE()
        self.date_time = datetime.datetime.now()
        # delete past values from future_df
        self.future_df = self.future_df[self.future_df['start_timestamp'] > self.date_time.now()]

        # find min 4 values of future_df
        self.future_df.sort_values(by=['marketprice'], inplace=True)
        self.future_df = self.future_df.iloc[:no_of_times]
        self.future_df.sort_values(by=['start_timestamp'], inplace=True)
        # add column
        self.future_df['triggerstatus'] = True
        print(self.future_df)
        # TODO: Put inside db

        return self.future_df

    def turn_on_turn_off(self):
        # TODO: get DB data and change to dataframe
        current_time = datetime.datetime.now()
        # Check if current time is within any interval
        while True:
            for index, row in self.future_df.iterrows():
                if not row['start_timestamp'] <= current_time <= row['end_timestamp']:
                    # print("True")
                    # Turn On
                    RelayControl().relayController(relayNumber=4, relayStatus=1)
                else:
                    # Turn OFF
                    RelayControl().relayController(relayNumber=4, relayStatus=0)
                    # print('False')


if __name__ == "__main__":
    auto_mode = Auto_Mode()
    auto_mode.auto_mode(4)
    auto_mode.turn_on_turn_off()
    print(auto_mode.future_df)

""""
    TODO
    Calculate the E value for "automode" every 24th hour and get the "master record"
    Calcualte the Escalation value with 1.33 static value
    Update this service
"""