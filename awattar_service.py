import pandas as pd
import datetime
from control import BulbControl
import requests

class AwattarService:
    def __init__(self):
        url = "https://api.awattar.at/v1/marketdata"
        marketdata_df = requests.get(url).json()
        self.one_day_df = pd.json_normalize(marketdata_df['data'])
        self.one_day_df['start_timestamp'] = pd.to_datetime(self.one_day_df['start_timestamp'], unit='ms')
        self.one_day_df['end_timestamp'] = pd.to_datetime(self.one_day_df['end_timestamp'], unit='ms')
        return None
    
    
    # def __init__(self):
    #     marketdata_df = pd.read_json('marketdata.json')
    #     marketdata_df = pd.json_normalize(marketdata_df['data'])

    #     # Convert 'start_timestamp' and 'end_timestamp' columns to datetime
    #     marketdata_df['start_timestamp'] = pd.to_datetime(marketdata_df['start_timestamp'], unit='ms')
    #     marketdata_df['end_timestamp'] = pd.to_datetime(marketdata_df['end_timestamp'], unit='ms')
    #     self.marketdata_df = marketdata_df
    #     self.bulb = BulbControl()

    # def update_marketdata(self):
    #     """
    #     This function updates the marketdata.json file and append to marketdata.csv
        
    #     Input: None
        
    #     Output: Boolean
        
    #     Usage:
    #         awattar_service = AwattarService()
    #         awattar_service.update_marketdata() --> True # This will append the current day data to the marketdata.csv file
    #             csv file.
    #     """

    #     url = "https://api.awattar.at/v1/marketdata"
    #     marketdata_df = requests.get(url).json()
    #     # marketdata_df.to_csv('marketdata.csv', index=False)
    #     one_day_df = pd.json_normalize(marketdata_df['data'])
    #     one_day_df.to_csv('marketdata.csv', mode='a', header=False, index=False)
    #     return True

    def check_market_price(self, eur:str):
        # This code runs whene current day max() price is less then 25% off
        creterion_timestamp = self.marketdata_df[self.marketdata_df['marketprice'] <= self.marketdata_df['marketprice'].max()*0.75]
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

    
    def get_average_awattar_price_over_period(self, start_time, end_time):
        """
        REPORT 4:
        This function returns the average price for a given time period
        
        Inputs:
            start_time: str eg: '2023-07-25 15:00:00'
            end_time: str eg: '2023-07-25 17:00:00'
        
        Output: average_price: float
        
        Usage:
            awattar_service = AwattarService()
            awattar_service.report_4('2023-07-25 15:00:00', '2023-07-25 17:00:00') --> 0.123
            
        """
        # Define the format of the string
        date_format = '%Y-%m-%d %H:%M:%S'
        try:
            start_time = datetime.datetime.strptime(start_time, date_format)
        except:
            print('start_time is not in the correct format')
            raise ValueError('start_time is not in the correct format')

        try:
            end_time = datetime.datetime.strptime(end_time, date_format)
        except:
            print('end_time is not in the correct format')
            raise ValueError('end_time is not in the correct format')
        
        # adding 1 hour to end_time to include the end_time
        end_time = end_time + datetime.timedelta(hours=1)
        filter_df = self.one_day_df[(self.one_day_df['start_timestamp'] >= start_time) & (self.one_day_df['end_timestamp'] <= end_time)]
        return filter_df['marketprice'].mean()