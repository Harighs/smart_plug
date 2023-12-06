import sys

sys.path.append('/home/pi/smart_plug/')
import os
import schedule
import time 
import subprocess

import sqlite3
from sqlite3 import Error

from datetime import datetime
import json

from flask import Flask, jsonify, request, send_file, render_template

import requests

from PIL import Image
import io
import pandas as pd
import matplotlib.pyplot as plt

from external_services.awattar_services import AwattarServices
from pi_controller.relay_controller import RelayControl
from external_services.smartmeter_services import SmartMeterServices
from database.db_manager import DatabaseManager
from main_services.common_utils import common_utils 
from main_services.auto_mode import Auto_Mode

from flask_paginate import Pagination, get_page_args

current_dir = os.getcwd()
print("Current working directory:", current_dir)

app = Flask(__name__)


"""
The following methods are used to display the html website
"""
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/infodatatable')
def infodatatable():
    api_url = f'http://{common_utils.static_ipaddress}:{common_utils.static_port}/api/datatable'
    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content of the response
            parsed_data = response.json()
        else:
            # Handle other status codes (e.g., render an error template)
            return render_template('error.html', error=f"Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., render an error template)
        return render_template('error.html', error=str(e))

    # Assuming the 'details.html' template expects a variable named 'data'
    return render_template('info_datatable.html', data=parsed_data)

@app.route('/infoautomoderelay')
def infoautomoderelay():
    api_url = f'http://{common_utils.static_ipaddress}:{common_utils.static_port}/api/automodestatus'
    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content of the response
            parsed_data = response.json()
        else:
            # Handle other status codes (e.g., render an error template)
            return render_template('error.html', error=f"Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., render an error template)
        return render_template('error.html', error=str(e))

    # Assuming the 'details.html' template expects a variable named 'data'
    return render_template('info_automoderelay.html', data=parsed_data)

@app.route('/infoautomode')
def infoautomode():
    api_url = f'http://{common_utils.static_ipaddress}:{common_utils.static_port}/api/automode'
    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content of the response
            parsed_data = response.json()
        else:
            # Handle other status codes (e.g., render an error template)
            return render_template('error.html', error=f"Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., render an error template)
        return render_template('error.html', error=str(e))

    # Assuming the 'details.html' template expects a variable named 'data'
    return render_template('info_automode.html', data=parsed_data)


@app.route('/infoservicestatus1')
def infoservicestatus1():
    api_url = f'http://{common_utils.static_ipaddress}:{common_utils.static_port}/api/getApiServiceStatus'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            parsed_data = response.json()
        else:
            return render_template('error.html', error=f"Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        return render_template('error.html', error=str(e))

    return render_template('info_servicestatus.html', parsed_data=parsed_data, title="API - Service Status")

@app.route('/infoservicestatus2')
def infoservicestatus2():
    api_url = f'http://{common_utils.static_ipaddress}:{common_utils.static_port}/api/getDataDownloadServiceStatus'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            parsed_data = response.json()
        else:
            return render_template('error.html', error=f"Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        return render_template('error.html', error=str(e))

    return render_template('info_servicestatus.html', parsed_data=parsed_data, title="Data Download - Service Status")


@app.route('/infoservicestatus3')
def infoservicestatus3():
    api_url = f'http://{common_utils.static_ipaddress}:{common_utils.static_port}/api/getAutoModeServiceStatus'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            parsed_data = response.json()
        else:
            return render_template('error.html', error=f"Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        return render_template('error.html', error=str(e))

    return render_template('info_servicestatus.html', parsed_data=parsed_data, title="AutoMode - Service Status")




"""
The following methods are used to serve the api  
"""
@app.route('/api/', methods=['GET'])
def api_home():
    return jsonify({"message": "Welcome to Enermizer API Services"}), 200



# New method to get the status if the services
@app.route('/api/status', methods=['GET'])
def rest_api():
    return jsonify({"status": "true"}), 200


# New method to insert the relay settings from app to database
@app.route('/api/postRelaySettings', methods=['POST'])
def postRelaySettings():
    json_data = request.json
    print("Received data:", json_data)

    try:
        relay1Power = json_data["relay1Power"]
        relay2Power = json_data["relay2Power"]

        db = DatabaseManager()
        db.insert_relaysettings_table(relay1Power, relay2Power)

    except Exception as e:
        print(f"An error occurred: {e}")
        return "", 400 # Server cannot process the request


    return jsonify({"status": "true"}), 200

@app.route('/api/datatable', methods=['GET'])
def getDataTable():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")

        df = pd.read_sql_query("SELECT * FROM datacache_report WHERE start_timestamp>=date('now', '-7 days') ORDER BY id DESC", conn)
        
        # Convert DataFrame to JSON
        json_data = df.to_json(orient='records')

        # Return JSON response
        return json_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "Error"}), 500

    finally:
        conn.close()

@app.route('/api/automodestatus', methods=['GET'])
def getAutoModeStatus():
    try:
        current_datetime = datetime.now()
        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_datetime.replace(hour=23, minute=59, second=59, microsecond=99)
        # Format datetime with 'T'
        start_of_day_str = start_of_day.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        end_of_day_str = end_of_day.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        # Connect to the SQLite database
        conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")

        query = f"SELECT REPLACE(start_timestamp, 'T', ' ') AS start_timestamp, REPLACE(end_timestamp, 'T', ' ') AS end_timestamp, marketprice, unit, relaynumber FROM automaterelay WHERE (start_timestamp >= '{start_of_day_str}' AND start_timestamp <= '{end_of_day_str}') OR (end_timestamp >= '{start_of_day_str}' AND end_timestamp <= '{end_of_day_str}')"

        df = pd.read_sql_query(query, conn)

        # Convert DataFrame to JSON
        json_data = df.to_json(orient='records')

        # Return JSON response
        return json_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "Error"}), 500

    finally:
          if 'conn' in locals() and conn:
            conn.close()

 
@app.route('/api/automode', methods=['GET'])
def getAutoMode():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")

        # Assuming you have a SQLite connection named 'conn'
        df = pd.read_sql_query(
            "SELECT SUBSTR(datetime, 1, INSTR(datetime, ' ') - 1) AS datetime, last_24hrs_usage, times_to_turnon, relaynumber FROM automode WHERE datetime >= date('now', '-7 days') ORDER BY id DESC",
            conn
        )

        # Convert DataFrame to JSON
        json_data = df.to_json(orient='records')

        # Return JSON response
        return json_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "Error"}), 500

    finally:
          if 'conn' in locals() and conn:
            conn.close()

 
@app.route('/api/datacache', methods=['GET'])
def getDataCache():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")
        cursor = conn.cursor()

        df = pd.read_sql_query("SELECT * FROM datacache_report WHERE start_timestamp>=date('now', '-7 days')", conn)

        # Check if the DataFrame is not empty
        if not df.empty:
            # Plot the DataFrame as a table

            # Calculate the figure size based on the number of rows and columns
            num_rows, num_cols = df.shape
            fig_width = num_cols * 2  # Adjust the multiplier as needed
            fig_height = num_rows * 0.2  # Adjust the multiplier as needed

            # Plot the DataFrame as a table
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            image_file = io.BytesIO()
            plt.savefig(image_file, format='png', bbox_inches='tight')
            image_file.seek(0)
            plt.close()
            if image_file:
                return send_file(image_file, mimetype='image/png')
            return jsonify({"status": "No data found"}), 404
            
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "Error"}), 500

    finally:
        conn.close()

# TODO add extra api methods to get the automode

# Define a function to get live relay status
def get_live_auto_relay_status():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("/home/pi/smart_plug/database/pythonsqlite.db")
        cursor = conn.cursor()

        df = pd.read_sql_query("SELECT start_timestamp, end_timestamp, marketprice, unit, relaynumber FROM automaterelay", conn)

        # Check if the DataFrame is not empty
        if not df.empty:
            # Plot the DataFrame as a table

            # Calculate the figure size based on the number of rows and columns
            num_rows, num_cols = df.shape
            fig_width = num_cols * 2  # Adjust the multiplier as needed
            fig_height = num_rows * 0.2  # Adjust the multiplier as needed

            # Plot the DataFrame as a table
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            image_file = io.BytesIO()
            plt.savefig(image_file, format='png', bbox_inches='tight')
            image_file.seek(0)
            plt.close()
            return image_file
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "Error"}), 500

    finally:
        conn.close()

# Define the API endpoint to get live relay status
@app.route('/api/liveAutoModeStatus', methods=['GET'])
def api_get_live_auto_relay_status():
    image_data = get_live_auto_relay_status()
    if image_data:
        return send_file(image_data, mimetype='image/png')
    return jsonify({"status": "No data found"}), 404


# New method to get all the reports from the database
@app.route('/api/getAllReports', methods=['POST'])
def getAllReports():
    json_data = request.json
    print("Received data:", json_data)
   
    try:
        from_date = datetime.strptime(json_data["fromDate"], "%Y-%m-%d")
        to_date = datetime.strptime(json_data["toDate"], "%Y-%m-%d")

        db = DatabaseManager()
        result = db.read_datacache_withdate_table(from_date, to_date)[0]

        if (result[0] is not None or result[3] is not None):
            # Create a dictionary with keys and values
            json_data = {
                "report1": str("{:.2f}".format(result[0])),
                "report2": str("{:.2f}".format(result[1])),
                "report3": str("{:.2f}".format(result[2])),
                "report4": str("{:.2f}".format(result[3])),
                "report5": str("{:.2f}".format(result[4]))
            }
        else:
            json_data = {
                "report1": "0",
                "report2": "0",
                "report3": "0",
                "report4": "0",
                "report5": "0",
            }
    except Exception as e:
        print(f"An error occurred: {e}")
        return "", 400 # Server cannot process the request
        # You might want to set a default value for json_data or handle the error in another way

    return jsonify({"message": str(json_data)}), 200


"""
 The following methods are used to control the RELAYs and its status
"""

@app.route('/api/relaystatus/<int:relayNumber>', methods=['POST'])
def relayStatus(relayNumber):
    relay_control = RelayControl()
    relay_status = relay_control.checkRelayStatus(relayNumber)
     # check if the relay is in auto mode
    db = DatabaseManager()
    results = db.read_relaymode_temp(relayNumber)
    if len(results) > 0:
        return jsonify({"status": str(bool(relay_status)), "relaystatus": "Auto"}), 200
    else:
        return jsonify({"status": str(bool(relay_status)), "relaystatus": str(bool(relay_status))}), 200


"""
Control the relay by passing switch number and switch status as parameter
"""

@app.route('/api/relaycontroller/<int:relayNumber>/<int:relayStatus>', methods=['POST'])
def relayController(relayNumber, relayStatus):
    relay_control = RelayControl()
    relay_trigger_status = relay_control.relayController(relayNumber, relayStatus)
    # check if the relay is in auto mode
    db = DatabaseManager()
    if(relayStatus == 0):
        print("when its on relay 2 off mode")
        db.insert_relaymode_report(relayNumber, "Off")
        db.delete_relaymode_temp(relayNumber)
    elif(relayStatus == 1):
        print("when its on relay 2 on mode")
        db.insert_relaymode_report(relayNumber, "On")
        db.delete_relaymode_temp(relayNumber)
    elif(relayStatus == 2):
        print("when its on relay 2 auto mode")
        db.insert_relaymode_report(relayNumber, "Auto")
        db.insert_relaymode_temp(relayNumber, "Auto")

    auto_mode = Auto_Mode()
    auto_mode.turn_on_turn_off(relayNumber)
    return jsonify({"status": str(bool(relay_trigger_status))}), 200

"""
The following methods are used to restart the services
"""

@app.route('/api/restartApiService', methods=['GET'])
def restartApiService(): 
    command1 = "sudo systemctl restart smart_plug.service"
    command2 = "sudo systemctl restart smart_plug.timer"

    result1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = subprocess.run(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    formatted_output1 = result1.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output1 = formatted_output1.replace('\n', ' ')  # Replaces newlines with spaces

    formatted_output2 = result2.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output2 = formatted_output2.replace('\n', ' ')  # Replaces newlines with spaces

    response_data = {
            "status": "True",
            "message": [formatted_output1,formatted_output2]
            }
    formatted_response = json.dumps(response_data, indent=4)

    if result1.returncode == 0:
        print("Command output:")

        return jsonify(json.loads(formatted_response)), 200

    else:
        print("Command failed with error:")
        return jsonify(json.loads(formatted_response)), 200
   

@app.route('/api/restartDataDownloadService', methods=['GET'])
def restartDatDownloadService():
    command1 = "sudo systemctl restart smart_plug_data_download.service"
    command2 = "sudo systemctl restart smart_plug_data_download.timer"

    result1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = subprocess.run(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    formatted_output1 = result1.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output1 = formatted_output1.replace('\n', ' ')  # Replaces newlines with spaces

    formatted_output2 = result2.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output2 = formatted_output2.replace('\n', ' ')  # Replaces newlines with spaces

    response_data = {
            "status": "True",
            "message": [formatted_output1,formatted_output2]
            }
    formatted_response = json.dumps(response_data, indent=4)

    if result1.returncode == 0:
        print("Command output:")

        return jsonify(json.loads(formatted_response)), 200

    else:
        print("Command failed with error:")
        return jsonify(json.loads(formatted_response)), 404
   

@app.route('/api/restartAutoModeService', methods=['GET'])
def restartAutoModeService():
    command1 = "sudo systemctl restart smart_plug_auto_mode.service"
    command2 = "sudo systemctl restart smart_plug_auto_mode.timer"

    result1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = subprocess.run(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    formatted_output1 = result1.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output1 = formatted_output1.replace('\n', ' ')  # Replaces newlines with spaces

    formatted_output2 = result2.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output2 = formatted_output2.replace('\n', ' ')  # Replaces newlines with spaces

    response_data = {
            "status": "True",
            "message": [formatted_output1,formatted_output2]
            }
    formatted_response = json.dumps(response_data, indent=4)

    if result1.returncode == 0:
        print("Command output:")

        return jsonify(json.loads(formatted_response)), 200

    else:
        print("Command failed with error:")
        return jsonify(json.loads(formatted_response)), 404
   
"""
The following method assists to check the status of the services
"""
@app.route('/api/getApiServiceStatus', methods=['GET'])
def getApiServiceStatus(): 
    command1 = "sudo systemctl status smart_plug.service"

    result1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    formatted_output1 = result1.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output1 = formatted_output1.replace('\n', ' ')  # Replaces newlines with spaces
    
    if result1.returncode == 0:
        response_data = {
            "status": "True",
            "message": [formatted_output1]
            }
    else:
         response_data = {
            "status": "False",
            "message": [formatted_output1]
            }

    formatted_response = json.dumps(response_data, indent=4)

    if result1.returncode == 0:
        print("Command output:")

        return jsonify(json.loads(formatted_response)), 200

    else:
        print("Command failed with error:")
        return jsonify(json.loads(formatted_response)), 404
   
    
@app.route('/api/getDataDownloadServiceStatus', methods=['GET'])
def getDatDownloadServiceStatus():
    command1 = "sudo systemctl status smart_plug_data_download.service"

    result1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    formatted_output1 = result1.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output1 = formatted_output1.replace('\n', ' ')  # Replaces newlines with spaces

    if result1.returncode == 0:
        response_data = {
            "status": "True",
            "message": [formatted_output1]
            }
    else:
         response_data = {
            "status": "False",
            "message": [formatted_output1]
            }

    formatted_response = json.dumps(response_data, indent=4)

    print("Command output:")

    return jsonify(json.loads(formatted_response)), 200


@app.route('/api/getAutoModeServiceStatus', methods=['GET'])
def getAutoModeServiceStatus():
    command1 = "sudo systemctl status smart_plug_auto_mode.service"

    result1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    formatted_output1 = result1.stdout.strip()  # Removes leading/trailing whitespace
    formatted_output1 = formatted_output1.replace('\n', ' ')  # Replaces newlines with spaces

    if result1.returncode == 0:
        response_data = {
            "status": "True",
            "message": [formatted_output1]
            }
    else:
         response_data = {
            "status": "False",
            "message": [formatted_output1]
            }

    formatted_response = json.dumps(response_data, indent=4)

    print("Command output:")

    return jsonify(json.loads(formatted_response)), 200


"""
 Main Python API service starts here
"""
if __name__ == '__main__':
    DatabaseManager()
    custom_ip = common_utils.static_ipaddress
    custom_port = common_utils.static_port
    app.run(host=custom_ip, port=custom_port, debug=True)