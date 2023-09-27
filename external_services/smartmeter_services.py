import requests
import pandas as pd
import json
from urllib.parse import quote

import datetime


class SmartMeterServices:
    def __init__(self):
        """
        This class is used to fetch data from the smartmeter.netz-noe.at website.
        
        Input: None
        
        Output:
            DataFrame: Returns a DataFrame with the following from json response from the website
            
        Usage:
            smartmeter = SmartMeter() --> Returns a SmartMeter object as Dataframe which can be stored
        """
        self.auth_url = 'https://smartmeter.netz-noe.at/orchestration/Authentication/Login'
        self.auth_payload = {"user": "SommererPrivatstiftung", "pwd": "SpS*1996"}
        self.auth_cookie, self.auth_xsrf_token, self.nsc_wt = self.post_request(self)
        return None

    # This method return the sum of consumed electricity data in Kwh
    def getConsolidatedData(self, start_date: str, end_date: str):
        """
        Usage:
            intrested_date: str --> '2023-8-24'
        
        Output:
            DataResonse['meteredValues'].sum() --> [float] kWh
        """
        if (start_date is None) or (end_date is None):
            raise Exception("Please provide a date in the format: Eg:'2023-8-24'")

        auth_cookie, auth_xsrf_token, nsc_wt = self.post_request(self)

        if auth_cookie and auth_xsrf_token is None:
            print("Authentication failed with status code:", self.auth_response.status_code)
        headers = {
            'Cookie': f'__Host-go4DavidSecurityToken={auth_cookie}; XSRF-Token={auth_xsrf_token}; NSC_WT_TWYUXFCQ-TTM={nsc_wt}',
        }

        self.data_url = f"https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Week?meterId=AT0020000000000000000000020826367&startDate={start_date}&endDate={end_date}"
        data_response = self.data_response(self, self.data_url, headers)
        if data_response is not None:
            data_response = pd.DataFrame(data_response)
            return data_response['meteredValues'].sum()

    # This method return the full data set of consumed electricity
    def getConsolidatedFullData(self, start_date: str, end_date: str):

        # Check the date format
        if (start_date is None) or (end_date is None):
            raise Exception("Please provide a 'start_date' and 'end_date' in the format: Eg:'2023-8-24'")

        if self.auth_cookie and self.auth_xsrf_token is None:
            print("Authentication failed with status code:", self.auth_response.status_code)
        headers = {
            'Cookie': f'__Host-go4DavidSecurityToken={self.auth_cookie};',
        }

        self.data_url = f"https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Week?meterId=AT0020000000000000000000020826367&startDate={start_date}&endDate={end_date}"
        data_response = self.data_response(self, self.data_url, headers)

        if data_response is not None:
            data_response = pd.DataFrame(data_response)[['meteredValues', 'peakDemandTimes']]
            return data_response.to_json()

    # This method returns the full data set consumed electricity of specific MeterId
    def getConsolidatedFullDataByMeterId(self, meter_id: str, start_date: str, end_date: str):

        # Check the date format
        if (start_date is None) or (end_date is None) or (meter_id is None):
            raise Exception("Please provide a 'start_date' and 'end_date' in the format: Eg:'2023-8-24'")

        if self.auth_cookie and self.auth_xsrf_token is None:
            print("Authentication failed with status code:", self.auth_response.status_code)
        headers = {
            'Cookie': f'__Host-go4DavidSecurityToken={self.auth_cookie};',
        }

        self.data_url = f"https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Week?meterId={meter_id}&startDate={start_date}&endDate={end_date}"
        data_response = self.data_response(self, self.data_url, headers)

        if data_response is not None:
            data_response = pd.DataFrame(data_response)[['meteredValues', 'peakDemandTimes']]
            return data_response.to_json()

    @staticmethod
    def post_request(self):
        auth_cookie, auth_xsrf_token, nsc_wt = None, None, None
        auth_response = requests.post(self.auth_url, json=self.auth_payload)
        if auth_response.status_code == 200:
            print("Authentication successful...")
            auth_cookie = auth_response.cookies['__Host-go4DavidSecurityToken']
            auth_xsrf_token = auth_response.cookies['XSRF-Token']
            nsc_wt = auth_response.cookies['NSC_WT_TWYUXFCQ-TTM']
            return auth_cookie, auth_xsrf_token, nsc_wt
        else:
            raise Exception("Authentication failed with status code: Smartmeter_service line 82",
                            self.auth_response.status_code)

    @staticmethod
    def data_response(self, data_url, headers):
        data_response = requests.get(data_url, headers=headers)
        if data_response.status_code == 200:
            return data_response.json()
        else:
            print("Data request failed with status code:", 'DATA FAILURE')
            raise Exception("Data request failed with status code: Smartmeter_service line 92",
                            data_response.status_code)

    # New func written on 22-09-2023
    def saving_SmartMeter_Data_Each_day(self):
        auth_url = 'https://smartmeter.netz-noe.at/orchestration/Authentication/Login'
        auth_payload = {"user": "SommererPrivatstiftung", "pwd": "SpS*1996"}
        auth_response = requests.post(auth_url, json=auth_payload)
        auth_cookie = auth_response.cookies['__Host-go4DavidSecurityToken']
        auth_xsrf_token = auth_response.cookies['XSRF-Token']
        current_date = str(datetime.date.today())
        data_url = "https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Day?meterId=AT0020000000000000000000020826368&day={}&__Host-go4DavidSecurityToken={}".format(current_date,auth_cookie)
        headers = {
            'Cookie': '__Host-go4DavidSecurityToken={}; XSRF-Token={}'.format(auth_cookie, auth_xsrf_token),
        }

        data_response = requests.get(data_url, headers=headers)

        if data_response.status_code == 200:
            print("The status code is 200 (OK).")
        else:
            raise ValueError(f"HTTP request is failing see this code with status code {data_response.status_code}.")


        new_data = pd.DataFrame(json.loads(data_response.content))[['meteredValues', 'peakDemandTimes']]

        # Convert all Unicode values in the DataFrame to regular strings
        for col in new_data.columns:
            new_data[col] = new_data[col].apply(lambda x: x.encode('utf-8') if isinstance(x, unicode) else x)
            if col == u'peakDemandTimes':
                new_data[u'peakDemandTimes'] = pd.to_datetime(new_data[u'peakDemandTimes'])

        smart_meter_data = pd.read_csv('smart_meter_data.csv')
        smart_meter_data[u'peakDemandTimes'] = pd.to_datetime(smart_meter_data[u'peakDemandTimes'])
        if smart_meter_data[u'peakDemandTimes'].max().date() < datetime.date.today():
            concatinated_data = pd.concat([smart_meter_data, new_data], ignore_index=True)

        #saving new data:
        concatinated_data.to_csv('smart_meter_data.csv', index=False)
        print("saving new data smartmeter data file to csv file")
        return True

    # New func written on 22-09-2023
    def get_smart_meter_data(self, start_date_time, end_date_time):
        """

        :param start_date_time: '2023-09-18 00:15:00'
        :param end_date_time: '2023-09-30 00:00:00'
        :return:
        """
        start_date = '2023-09-18 00:15:00'
        end_date = '2023-09-30 00:00:00'

        # Define the start_date and end_date
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        smart_meter_data = pd.read_csv('smart_meter_data.csv')  # Read in the DataFrame
        # Filter the DataFrame for rows within the desired datetime range
        filtered_df = smart_meter_data[(smart_meter_data['peakDemandTimes'] >= start_date) & (smart_meter_data['peakDemandTimes'] <= end_date)]

        # Calculate the mean of 'meteredValues' for the filtered rows
        return filtered_df['meteredValues'].mean()
