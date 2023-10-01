import os
import schedule
import time
from datetime import datetime
from flask import Flask, jsonify, request

from database.db_manager import DatabaseManager
from external_services.awattar_services import AwattarServices
from pi_controller.relay_controller import RelayControl

current_dir = os.getcwd()
print("Current working directory:", current_dir)

app = Flask(__name__)


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
        return "", 400  # Server cannot process the request

    return jsonify({"status": "true"}), 200


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
        return "", 400  # Server cannot process the request
        # You might want to set a default value for json_data or handle the error in another way

    return jsonify({"message": str(json_data)}), 200


"""
 The following methods are used to control the RELAYs and its status
"""


@app.route('/api/relaystatus/<int:relayNumber>', methods=['POST'])
def relayStatus(relayNumber):
    relay_control = RelayControl()
    relay_status = relay_control.checkRelayStatus(relayNumber)
    return jsonify({"status": str(bool(relay_status))}), 200


"""
Control the relay by passing switch number and switch status as parameter
"""


@app.route('/api/relaycontroller/<int:relayNumber>/<int:relayStatus>', methods=['POST'])
def relayController(relayNumber, relayStatus):
    relay_control = RelayControl()
    relay_trigger_status = relay_control.relayController(relayNumber, relayStatus)
    return jsonify({"status": str(bool(relay_trigger_status))}), 200


"""
 Extra methods and apis
"""


# Define the function to download awattar data
def download_awattar_data():
    awattar_service = AwattarServices()
    return None


# Schedule the download_awattar_data function to run at 12-hour intervals
schedule.every(12).hours.do(download_awattar_data)

"""
 Main Python API service starts here
"""
if __name__ == '__main__':

    """
    TODO 
    Once this service is started and then the following should automatically called
    1. Get daily awattar dataset and store it on our local sqlite database
    2. Get daily consumption and store it on our local sqlite database
    3. then we have all data at one place --> sqlite database and now its easier to calculate the 
        reports.    
    Better call another service from here to avoid the crashes.
    """

    custom_ip = '192.168.1.238'
    custom_port = 8080
    app.run(host=custom_ip, port=custom_port, debug=True)

    download_awattar_data = AwattarServices().download_awattar_data()

    # Run the scheduler loop in a separate thread
    while True:
        schedule.run_pending()
        time.sleep(1)
