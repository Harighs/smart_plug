import sys 
sys.path.append('/home/pi/smart_plug/')
import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from main_services.common_utils import common_utils 
import pytz
import time 

class AwattarServices:
    def __init__(self):
        self.dataset_path = '/home/pi/smart_plug/dataset/awattar_data.csv'
        self.awattar_json_url = "https://api.awattar.at/v1/marketdata?start={}&end={}"
        # self.download_awattar_data()
        # if not os.path.isfile(self.dataset_path):
        #    raise Exception('Dataset not found')
        return None

    def check_market_price(self, eur: str):
        # This code runs whene current day max() price is less then 25% off
        creterion_timestamp = self.marketdata_df[
            self.marketdata_df['marketprice'] <= self.marketdata_df['marketprice'].max() * 0.75]
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
        try:
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        except:
            print('start_time is not in the correct format')
            raise ValueError('start_time is not in the correct format')

        try:
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        except:
            print('end_time is not in the correct format')
            raise ValueError('end_time is not in the correct format')

        # adding 1 hour to end_time to include the end_time

        end_time = end_time + datetime.timedelta(hours=1)
        df = pd.read_csv(self.dataset_path)
        df['start_timestamp'] = pd.to_datetime(df['start_timestamp'])
        df['end_timestamp'] = pd.to_datetime(df['end_timestamp'])
        filter_df = df[(df['start_timestamp'] >= start_time) & (df['end_timestamp'] <= end_time)]
        return filter_df['marketprice'].mean()

    def download_awattar_data(self):
        # New data
        url = "https://api.awattar.at/v1/marketdata"
        new_df = requests.get(url).json()
        new_df = pd.json_normalize(new_df['data'])
        new_df['start_timestamp'] = pd.to_datetime(new_df['start_timestamp'], unit='ms')
        new_df['end_timestamp'] = pd.to_datetime(new_df['end_timestamp'], unit='ms')

        # Check if the file exists
        if not os.path.isfile(self.dataset_path):
            new_df.to_csv(self.dataset_path, index=True)
            return None

        old_df = pd.read_csv(self.dataset_path)
        old_df['start_timestamp'] = pd.to_datetime(old_df['start_timestamp'])
        old_df['end_timestamp'] = pd.to_datetime(old_df['end_timestamp'])

        old_end_date = old_df['end_timestamp'].max()
        new_start_date = new_df['start_timestamp'].min()

        if old_end_date == new_start_date:
            print('No new data available')
            return None

        elif old_end_date < new_start_date:
            # Saving the new data
            print('New data available... saving the new data')
            resulting_df = pd.concat([old_df, new_df], ignore_index=True)
            resulting_df.to_csv(self.dataset_path, index=True)

    def AWATTAR_ONE_DAY_PERIOD(self):
        # Delete the awattar_data csv before creation
        Awattar_Data_Path = '/home/pi/smart_plug/dataset/'+common_utils.static_awattar_filename
        if os.path.exists(Awattar_Data_Path):
            os.remove(Awattar_Data_Path)

        # This return the datetime timestamp before 24hours
        # Replace this with your Unix timestamp
        current_datetime = datetime.now() - timedelta(hours=24)
        unix_timestamp = current_datetime.timestamp()
        start_of_day, end_of_day = AwattarServices.get_start_and_end_of_day(unix_timestamp)

        # Get Awattar Data
        json_url = self.awattar_json_url.format(int(start_of_day.timestamp() * 1000),
                                                int(end_of_day.timestamp() * 1000))
        awattar_json_response = requests.get(json_url).json()
        awattar_json_response = pd.json_normalize(awattar_json_response['data'])
        awattar_json_response['start_timestamp'] = pd.to_datetime(awattar_json_response['start_timestamp'], unit='ms') + pd.Timedelta(hours=1)
        awattar_json_response['end_timestamp'] = pd.to_datetime(awattar_json_response['end_timestamp'], unit='ms') + pd.Timedelta(hours=1)

        if os.path.exists(self.dataset_path):
            os.remove(self.dataset_path)
        awattar_json_response.to_csv(self.dataset_path, index=False)
        return awattar_json_response

    def AWATTAR_FUTURE_PRICE(self):

        timezone = 'Europe/Vienna'  # Replace with your desired timezone

        start_of_day, end_of_day = AwattarServices.get_start_and_end_of_day(timezone)

        print(f"Awattar After Start of the day: {start_of_day}")
        print(f"Awattar After End of the day: {end_of_day}")

        # Get Awattar Data
        json_url = self.awattar_json_url.format(start_of_day, end_of_day)
        
        awattar_json_response = requests.get(json_url).json()
        awattar_json_response = pd.json_normalize(awattar_json_response['data'])
        awattar_json_response['start_timestamp'] = pd.to_datetime(awattar_json_response['start_timestamp'], unit='ms') + pd.Timedelta(hours=1)
        awattar_json_response['end_timestamp'] = pd.to_datetime(awattar_json_response['end_timestamp'], unit='ms') + pd.Timedelta(hours=1)

        if os.path.exists(self.dataset_path):
            os.remove(self.dataset_path)
        awattar_json_response.to_csv(self.dataset_path, index=False)
        return awattar_json_response
    

    def get_start_and_end_of_day(timezone='CET'):
        timestamp = time.time() * 1000  # Current timestamp in milliseconds

        # Convert timestamp to datetime object
        dt_object = datetime.utcfromtimestamp(timestamp / 1000)

        # Set the timezone to UTC
        dt_object_utc = pytz.timezone('UTC').localize(dt_object)

        # Convert UTC to the specified local time zone
        dt_object_local = dt_object_utc.astimezone(pytz.timezone(timezone))

        # Get the start and end of the day
        start_of_day = dt_object_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Convert datetime objects to Unix timestamps in milliseconds
        start_timestamp = int(start_of_day.timestamp()) * 1000
        end_timestamp = int(end_of_day.timestamp()) * 1000
        
        print(f"Start of the day: {start_of_day}")
        print(f"End of the day: {end_of_day}")

        return start_timestamp, end_timestamp

