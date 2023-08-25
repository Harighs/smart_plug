import requests
import pandas as pd
from urllib.parse import quote


class SmartMeter():
    def __init__(self):
        """
        This class is used to fetch data from the smartmeter.netz-noe.at website.
        
        Input: None
        
        Output:
            DataFrame: Returns a DataFrame with the following from json response from the website
            
        Usage:
            smartmeter = SmartMeter() --> Returns a SmartMeter object as Dataframe which can be stored
        """   
        # URL for authentication
        # self.auth_url = 'https://smartmeter.netz-noe.at/orchestration/Authentication/Login'
        # self.auth_payload = {"user": "SommererPrivatstiftung", "pwd": "SpS*1996"}
        
        # if self.post_request(self):
        #     print("Authentication successful")
        #     auth_cookie = self.auth_response.cookies['__Host-go4DavidSecurityToken']
        #     auth_xsrf_token = self.auth_response.cookies['XSRF-Token']

        #     # URL for fetching data
        #     data_url = f"https://smartmeter.netz-noe.at/orchestration/User/GetMeteringPointByAccountId?accountId=000019014443"
            
        #     headers = {
        #         'Cookie': f'__Host-go4DavidSecurityToken={auth_cookie}; XSRF-Token={auth_xsrf_token}',
        #     }
            
        #     if self.data_response(self, data_url, headers):
        #         data_response = requests.get(data_url, headers=headers).json()
        #         self.SMART_METER_DATA = pd.DataFrame(data_response[0])
        #         (self.SMART_METER_DATA)
        #         print("HARI ---- SUCESS#######################")
        #     else:
        #         print("Data request failed with status code:", 'DATA FAILURE')
        # else:
        #     print("Authentication failed with status code:", self.auth_response.status_code)
        return None
    
    def get_data(self):
        auth_url = 'https://smartmeter.netz-noe.at/orchestration/Authentication/Login'
        auth_payload = {"user": "SommererPrivatstiftung", "pwd": "SpS*1996"}

        auth_response = requests.post(auth_url, json=auth_payload)
        auth_cookie = auth_response.cookies['__Host-go4DavidSecurityToken']
        auth_xsrf_token = auth_response.cookies['XSRF-Token']
        ### TODO: update date from mobile 
        
        data_url = f"https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Day?meterId=AT0020000000000000000000020826368&day=2023-8-24&__Host-go4DavidSecurityToken={auth_cookie}"

        headers = {
            'Cookie': f'__Host-go4DavidSecurityToken={auth_cookie}; XSRF-Token={auth_xsrf_token}',
        }

        data_response = requests.get(data_url, headers=headers).json()
        data = pd.DataFrame(data_response)
        data = data['meteredValues'].sum()
        return data
    
    @staticmethod
    def post_request(self):
        self.auth_response = requests.post(self.auth_url, json=self.auth_payload)
        if self.auth_response.status_code == 200:
            return True
        
    @staticmethod
    def data_response(self, data_url, headers):
        data_response = requests.get(data_url, headers=headers)
        if data_response.status_code == 200:
            return True
        else:
            return False
                
