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
        self.auth_url = 'https://smartmeter.netz-noe.at/orchestration/Authentication/Login'
        self.auth_payload = {"user": "SommererPrivatstiftung", "pwd": "SpS*1996"}
        return None
    
    def get_data(self, intrested_date: str = None):
        """
        Usage:
            intrested_date: str --> '2023-8-24'
        
        Output:
            DataResonse['meteredValues'].sum() --> [float] kWh
        """
        
        auth_cookie, auth_xsrf_token = self.post_request(self)
        
        if auth_cookie and auth_xsrf_token is None:
            print("Authentication failed with status code:", self.auth_response.status_code)
        headers = {
            'Cookie': f'__Host-go4DavidSecurityToken={auth_cookie}; XSRF-Token={auth_xsrf_token}',
        }
        if intrested_date is None:
            intrested_date = '2023-8-24'
            
        ### TODO: update date from mobile 
        self.data_url = f"https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Day?meterId=AT0020000000000000000000020826368&day={intrested_date}&__Host-go4DavidSecurityToken={auth_cookie}"
        data_response = self.data_response(self, self.data_url, headers)
        if data_response is not None:
            data_response = pd.DataFrame(data_response)
            return data_response['meteredValues'].sum()

    
    @staticmethod
    def post_request(self):
        auth_response = requests.post(self.auth_url, json=self.auth_payload)
        if auth_response.status_code == 200:
            print("Authentication successful...")
            auth_cookie = auth_response.cookies['__Host-go4DavidSecurityToken']
            auth_xsrf_token = auth_response.cookies['XSRF-Token']
            return auth_cookie, auth_xsrf_token
        else:
            raise Exception("Authentication failed with status code: Smartmeter_service line 74", self.auth_response.status_code)
            
        
    @staticmethod
    def data_response(self, data_url, headers):
        data_response = requests.get(data_url, headers=headers).json()
        if data_response.status_code == 200:
            return data_response
        else:
            print("Data request failed with status code:", 'DATA FAILURE')
            raise Exception("Data request failed with status code: Smartmeter_service line 84", data_response.status_code)
                
