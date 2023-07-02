import datetime

import pandas as pd

from raspberrypi_controller import BulbControl, enable_relay1, disable_relay1

"""
    This class is responsible for handling and accessing the backend services.
    For example: 
        - Accessing the awattar api services and retrieves the next 24 hours price dataset
        - Based on the market price trigger the relays and change it status
"""


class AwattarService:
    def __init__(self):
        marketdata_df = pd.read_json('marketdata.json')
        marketdata_df = pd.json_normalize(marketdata_df['data'])

        # Convert 'start_timestamp' and 'end_timestamp' columns to datetime
        marketdata_df['start_timestamp'] = pd.to_datetime(marketdata_df['start_timestamp'], unit='ms')
        marketdata_df['end_timestamp'] = pd.to_datetime(marketdata_df['end_timestamp'], unit='ms')
        self.marketdata_df = marketdata_df
        self.bulb = BulbControl()

    def check_market_price(self, euro: str):
        # This code runs when current day max() price is less than 25% offer
        # creterion_timestamp = self.marketdata_df[self.marketdata_df['marketprice'] <= self.marketdata_df['marketprice'].max()*0.75]

        # Base on the euro parameter the relays will be activated
        creterion_timestamp = self.marketdata_df[self.marketdata_df['marketprice'] <= int(euro)]
        # Get the current time
        current_time = datetime.datetime.now().time()

        print("Current Time: ", current_time)
        print("Current Data-set: ", creterion_timestamp)
        print("Chosen Euro: ", int(euro))

        # Iterate over the rows of the DataFrame
        for _, row in creterion_timestamp.iterrows():
            start_time = row['start_timestamp'].time()
            end_time = row['end_timestamp'].time()

            # Check if the current time is within the start and end time for the current row
            if start_time <= current_time <= end_time:
                print('Current time is between start and end time for row', _)
                enable_relay1()
                break
                # bulb on
            else:
                print('Price is too high')
                disable_relay1()
                continue
