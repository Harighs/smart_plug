import datetime

import pandas as pd

from control import BulbControl


class AwattarService:
    def __init__(self):
        marketdata_df = pd.read_json('marketdata.json')
        marketdata_df = pd.json_normalize(marketdata_df['data'])

        # Convert 'start_timestamp' and 'end_timestamp' columns to datetime
        marketdata_df['start_timestamp'] = pd.to_datetime(marketdata_df['start_timestamp'], unit='ms')
        marketdata_df['end_timestamp'] = pd.to_datetime(marketdata_df['end_timestamp'], unit='ms')
        self.marketdata_df = marketdata_df
        self.bulb = BulbControl()

    def check_market_price(self, eur: str):
        # This code runs whene current day max() price is less then 25% off
        # creterion_timestamp = self.marketdata_df[self.marketdata_df['marketprice'] <= self.marketdata_df['marketprice'].max()*0.75]
        creterion_timestamp = self.marketdata_df[self.marketdata_df['marketprice'] <= int(eur)]
        # Get the current time
        current_time = datetime.datetime.now().time()
        print(current_time)
        print(creterion_timestamp)
        print(int(eur))
        # Iterate over the rows of the DataFrame
        for _, row in creterion_timestamp.iterrows():
            start_time = row['start_timestamp'].time()
            end_time = row['end_timestamp'].time()

            # Check if the current time is within the start and end time for the current row

            if start_time <= current_time <= end_time:
                print('Current time is between start and end time for row', _)
                self.bulb.bulb_on()
                break
                # bulb on
            else:
                print('Price is too high')
                self.bulb.bulb_off()
                continue
