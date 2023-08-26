import requests
import pandas as pd
from urllib.parse import quote


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
