#!/usr/bin/python3

import datetime

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

print(f"Hello, world! Current date and time: {formatted_datetime}")