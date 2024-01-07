import sys 
sys.path.append('/home/pi/smart_plug/')
import datetime
import json
import os
import pandas as pd
import requests

from main_services.common_utils import common_utils 

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
        # self.auth_url = common_utils.static_smart_meter_service_link+'orchestration/Authentication/Login'
        # self.auth_payload = {"user": common_utils.static_smart_meter_username, "pwd": common_utils.static_smart_meter_password}
        # self.auth_cookie, self.auth_xsrf_token, self.nsc_wt = self.post_request(self)
        self.dataset_path = '/home/pi/smart_plug/dataset/'+common_utils.static_smartmeter_filename

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

        self.data_url = f"{common_utils.static_smart_meter_service_link}orchestration/ConsumptionRecord/Week?meterId={common_utils.static_smart_meter_meter_id}&startDate={start_date}&endDate={end_date}"
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

        self.data_url = f"{common_utils.static_smart_meter_service_link}orchestration/ConsumptionRecord/Week?meterId={common_utils.static_smart_meter_meter_id}&startDate={start_date}&endDate={end_date}"
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

        self.data_url = f"{common_utils.static_smart_meter_service_link}orchestration/ConsumptionRecord/Week?meterId={meter_id}&startDate={start_date}&endDate={end_date}"
        data_response = self.data_response(self, self.data_url, headers)

        if data_response is not None:
            data_response = pd.DataFrame(data_response)[['meteredValues', 'peakDemandTimes']]
            return data_response.to_json()

    @staticmethod
    def post_request(self):
        auth_cookie, auth_xsrf_token, nsc_wt = None, None, None
        auth_response = requests.post(self.auth_url, json=self.auth_payload)
        if auth_response.status_code == 200:
            print("Smart meter - Authentication successful...")
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

    # Currently used to download the smart-meter data
    # update 18.11.23
    def sm_each_date(self):
        # Delete the smartmeter_data csv before creation
        SmartMeter_Data_Path = '/home/pi/smart_plug/dataset/'+common_utils.static_smartmeter_filename
        if os.path.exists(SmartMeter_Data_Path):
            os.remove(SmartMeter_Data_Path)

        auth_url = common_utils.static_smart_meter_service_link+'orchestration/Authentication/Login'
        auth_payload = {"user": common_utils.static_smart_meter_username, "pwd": common_utils.static_smart_meter_password}
        auth_response = requests.post(auth_url, json=auth_payload)
        auth_cookie = auth_response.cookies['__Host-go4DavidSecurityToken']
        auth_xsrf_token = auth_response.cookies['XSRF-Token']
        nsc_wt = auth_response.cookies['NSC_WT_TWYUXFCQ-TTM']

        current_date = str(
            datetime.date.today() - datetime.timedelta(days=1))  # last 24hrs data
        # TODO remove the hardcoded meter id or id
        data_url = f"{common_utils.static_smart_meter_service_link}orchestration/ConsumptionRecord/Day?meterId={common_utils.static_smart_meter_meter_id}&day={current_date}&__Host-go4DavidSecurityToken={auth_cookie}"
        #data_url = "https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/BalanceDay?pointOfConsumption=41151064&day={}&__Host-go4DavidSecurityToken={}".format(current_date,auth_cookie)
        #data_url =  "https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/BalanceDay?pointOfConsumption=41151064&day=2023-12-22"
        headers = {
            'Cookie': '__Host-go4DavidSecurityToken={}; XSRF-Token={}; NSC_WT_TWYUXFCQ-TTM={};'.format(auth_cookie, auth_xsrf_token, nsc_wt),
        }

        data_response = requests.get(data_url, headers=headers)

        if data_response.status_code == 200:
            print("The status code is 200 (OK).")
        else:
            raise ValueError(f"HTTP request is failing see this code with status code {data_response.status_code}.")
        
        # Datetime
        # Get the current date
        current_date = str(datetime.date.today() - datetime.timedelta(days=1))

        # Combine with the time '00:00:00'
        combined_datetime = pd.to_datetime(current_date + ' 00:00:00')
        """ 
                # Default dataset
                default_data = {'meteredValues': [0],
                        'peakDemandTimes': [combined_datetime]}

                # Create a DataFrame from the default dataset
                default_df = pd.DataFrame(default_data)
        """
        
        new_data = pd.DataFrame(json.loads(data_response.content))[['meteredValues', 'peakDemandTimes']]
        # Convert 'peakDemandTimes' to datetime and add 1 hour
        new_data['peakDemandTimes'] = pd.to_datetime(new_data['peakDemandTimes']) + pd.Timedelta(hours=1)

        # Concatenate the default data and the loaded data
        # final_data = pd.concat([default_df, new_data], ignore_index=True)

        if os.path.exists(self.dataset_path):
            os.remove(self.dataset_path)
        new_data.to_csv(self.dataset_path, index=False)

        # Logout the smart meter service
        # https://smartmeter.netz-noe.at/orchestration/Authentication/Logout
        auth_logout_url = common_utils.static_smart_meter_service_link+'orchestration/Authentication/Logout'
        auth_response = requests.get(auth_logout_url, headers=headers)
        if auth_response.status_code == 200:
            print("Logout success.")
        else:
            print("Logout failed.")

        return new_data

    def saving_SmartMeter_Data_Each_day(self):
        auth_url = common_utils.static_smart_meter_service_link+'orchestration/Authentication/Login'
        auth_payload = {"user": common_utils.static_smart_meter_username, "pwd": common_utils.static_smart_meter_password}
        auth_response = requests.post(auth_url, json=auth_payload)
        auth_cookie = auth_response.cookies['__Host-go4DavidSecurityToken']
        auth_xsrf_token = auth_response.cookies['XSRF-Token']
        current_date = str(datetime.date.today())
        data_url = f"{common_utils.static_smart_meter_service_link}orchestration/ConsumptionRecord/Day?meterId={common_utils.static_smart_meter_meter_id}&day={current_date}&__Host-go4DavidSecurityToken={auth_cookie}"
        headers = {
            'Cookie': '__Host-go4DavidSecurityToken={}; XSRF-Token={}'.format(auth_cookie, auth_xsrf_token),
        }

        data_response = requests.get(data_url, headers=headers)

        if data_response.status_code == 200:
            print("The status code is 200 (OK).")
        else:
            raise ValueError(f"HTTP request is failing see this code with status code {data_response.status_code}.")

        new_data = pd.DataFrame(json.loads(data_response.content.decode('utf-8')))[['meteredValues', 'peakDemandTimes']]

        # Convert all Unicode values in the DataFrame to regular strings
        for col in new_data.columns:
            if col == u'peakDemandTimes':
                new_data[u'peakDemandTimes'] = pd.to_datetime(new_data[u'peakDemandTimes'])

        smart_meter_data = pd.read_csv('/home/pi/smart_plug/dataset/'+common_utils.static_smartmeter_filename)
        smart_meter_data[u'peakDemandTimes'] = pd.to_datetime(smart_meter_data[u'peakDemandTimes'])
        if smart_meter_data[u'peakDemandTimes'].max().date() < datetime.date.today():
            concatinated_data = pd.concat([smart_meter_data, new_data], ignore_index=True)

        # saving new data:
        concatinated_data.to_csv('/home/pi/smart_plug/dataset/'+common_utils.static_smartmeter_filename, index=False)
        print("saving new data smartmeter data file to csv file")
        return concatinated_data

    # New func written on 22-09-2023
    def get_smart_meter_data(self, start_date_time, end_date_time):
        """

        :param start_date_time: '2023-09-18 00:15:00'
        :param end_date_time: '2023-09-30 00:00:00'
        :return:
        """
        path_to_file = '/home/pi/smart_plug/dataset/'+common_utils.static_smartmeter_filename

        # Define the start_date and end_date
        start_date = pd.to_datetime(start_date_time)
        end_date = pd.to_datetime(end_date_time)
        smart_meter_data = pd.read_csv(path_to_file)  # Read in the DataFrame
        for col in smart_meter_data.columns:
            if col == u'peakDemandTimes':
                smart_meter_data[u'peakDemandTimes'] = pd.to_datetime(smart_meter_data[u'peakDemandTimes'])
        # Filter the DataFrame for rows within the desired datetime range
        filtered_df = smart_meter_data[
            (smart_meter_data[u'peakDemandTimes'] >= start_date) & (smart_meter_data[u'peakDemandTimes'] <= end_date)]
        # Calculate the mean of 'meteredValues' for the filtered rows
        return filtered_df['meteredValues'].mean()


    def getSmartMeterDataFromYesterday(self):
        ## SMART METER STEP1: Login into smart-meter
        auth_url = common_utils.static_smart_meter_service_link+'orchestration/Authentication/Login'
        auth_payload = {"user": common_utils.static_smart_meter_username, "pwd": common_utils.static_smart_meter_password}
        auth_response = None

        auth_cookie, auth_xsrf_token, nsc_wt = None, None, None
        auth_response = requests.post(auth_url, json=auth_payload)
        all_cookies = None

        if auth_response.status_code == 200:
            print("The status code is 200 (OK).")
            print("Smart meter - Authentication successful...")
            all_cookies = auth_response.cookies
            auth_cookie = auth_response.cookies['__Host-go4DavidSecurityToken']
            auth_xsrf_token = auth_response.cookies['XSRF-Token']
            nsc_wt = auth_response.cookies['NSC_WT_TWYUXFCQ-TTM']
        else:
            raise Exception("Authentication failed with status code: getSmartMeterDataFromYesterday",auth_response.status_code)


        headers = {
            'Cookie': f'__Host-go4DavidSecurityToken={auth_cookie};XSRF-Token={auth_xsrf_token};NSC_WT_TWYUXFCQ-TTM={nsc_wt};',
        }

        ## SMART METER STEP2: Get data from smart-meter reading
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        print("SMART METER STEP2: Get data from smart-meter reading:", yesterday)

        data_url = f"{common_utils.static_smart_meter_service_link}orchestration/ConsumptionRecord/Day?meterId={common_utils.static_smart_meter_meter_id}&day={yesterday}"
        data_response = requests.get(data_url, headers=headers)
        outputData = None
        print("SMART METER :", data_url)

        if data_response.status_code == 200:
            outputData = pd.DataFrame(json.loads(data_response.content))[['meteredValues', 'peakDemandTimes']]
             # Convert 'peakDemandTimes' to datetime and add 1 hour
            outputData['peakDemandTimes'] = pd.to_datetime(outputData['peakDemandTimes']) + pd.Timedelta(hours=1)
            print("Output Data From SmartMeter:", outputData)

            ## Export to CSV
            if os.path.exists(self.dataset_path):
                os.remove(self.dataset_path)
            outputData.to_csv(self.dataset_path, index=False)

        else:
            print("Data request failed with status code:", 'DATA FAILURE')
            raise Exception("Data request failed with status code: Smartmeter_service2", data_response.status_code)

        # Logout the smart meter service
        # https://smartmeter.netz-noe.at/orchestration/Authentication/Logout
        auth_logout_url = common_utils.static_smart_meter_service_link+'orchestration/Authentication/Logout'
        auth_response = requests.get(auth_logout_url, headers=headers)
        if auth_response.status_code == 200:
            print("Logout success.")
        else:
            print("Logout failed.")


        if len(outputData) > 0:
            print("Data fetch success.")
            return outputData
        else:
            raise Exception("Data request failed with status code: Smartmeter_service2", 404)


if __name__ == '__main__':
    smartMeterServices = SmartMeterServices()
    smartMeterServices.getSmartMeterDataFromYesterday()