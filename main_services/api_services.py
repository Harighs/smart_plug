from datetime import datetime

from flask import Flask, jsonify, request
import sys
sys.path.append('../')
import os
from main_services.relay_controller import RelayControl
from database.db_manager import DatabaseManager

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
        return "", 400 # Server cannot process the request


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
    results = db.read_automode_temp(relayNumber)
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
    if(relayStatus == 2):
        db = DatabaseManager()
        db.insert_automode(relayNumber)
    else:
        db = DatabaseManager()
        db.delete_automode_temp(relayNumber)

    return jsonify({"status": str(bool(relay_trigger_status))}), 200


"""
 Main Python API service starts here
"""
if __name__ == '__main__':

    custom_ip = '192.168.1.238'
    custom_port = 8080
    app.run(host=custom_ip, port=custom_port, debug=True)
