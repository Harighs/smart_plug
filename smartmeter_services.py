import requests
import pandas as pd


class SmartMeter():
    def __init__(self):           
        # URL for authentication
        self.auth_url = 'https://smartmeter.netz-noe.at/orchestration/Authentication/Login'
        self.auth_payload = {"user": "SommererPrivatstiftung", "pwd": "SpS*1996"}

    def post_request(self):
        self.auth_response = requests.post(self.auth_url, json=self.auth_payload)
                
        if self.auth_response.status_code == 200:
            auth_cookie = self.auth_response.cookies['__Host-go4DavidSecurityToken']
            auth_xsrf_token = self.auth_response.cookies['XSRF-Token']

            # URL for fetching data
            data_url = f"https://smartmeter.netz-noe.at/orchestration/User/GetMeteringPointByAccountId?accountId=000019014443"
            
            headers = {
                'Cookie': f'__Host-go4DavidSecurityToken={auth_cookie}; XSRF-Token={auth_xsrf_token}',
            }
            
            data_response = requests.get(data_url, headers=headers)
            
            if data_response.status_code == 200:
                data = data_response.json()
                # Process the data as needed
                df = pd.DataFrame(data[0])
                return df
            else:
                print("Data request failed with status code:", data_response.status_code)
                return None
        else:
            print("Authentication failed with status code:", self.auth_response.status_code)
            return None
