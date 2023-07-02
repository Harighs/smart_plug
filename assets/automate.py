import pandas as pd
import json
import numpy as np
import time
import datetime
import os


from control import BulbControl
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
import os
os.system("!curl 'https://api.awattar.at/v1/marketdata' -o 'marketdata.json'")

marketdata_df = pd.read_json('marketdata.json')
marketdata_df = pd.json_normalize(marketdata_df['data'])

# Convert 'start_timestamp' and 'end_timestamp' columns to datetime
marketdata_df['start_timestamp'] = pd.to_datetime(marketdata_df['start_timestamp'], unit='ms')
marketdata_df['end_timestamp'] = pd.to_datetime(marketdata_df['end_timestamp'], unit='ms')


creterion_timestamp  = marketdata_df[marketdata_df['marketprice'] >= marketdata_df['marketprice'].max()]

bulb = BulbControl()
while True:
    # Get the current time
    current_time = datetime.datetime.now().time()

    # Iterate over the rows of the DataFrame
    for _, row in creterion_timestamp.iterrows():
        if row['start_timestamp'].time() <= current_time <= row['end_timestamp'].time():
            print('filter is okey', _)
            bulb.bulb_on()
            break

        else:
            print('current time is not in filter')
            bulb.bulb_off()

    # Wait for some time before checking again
    time.sleep(60)  # Sleep for 60 seconds (adjust as needed)
    
    