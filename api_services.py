import os
import schedule
import time

from flask import Flask, jsonify, request

from external_services.awattar_services import AwattarServices
from pi_controller.relay_controller import RelayControl
from external_services.smartmeter_services import SmartMeterServices

current_dir = os.getcwd()
print("Current working directory:", current_dir)

app = Flask(__name__)


# API SERVICE STATUS
@app.route('/api/status', methods=['GET'])
def rest_api():
    return jsonify({"status": "true"}), 200


"""
    # SMART METER SERVICES
    The following methods are used to retrieve the data from SMART METER SERVICES
"""


# Report 1 - Energy consumed over selected time period
@app.route('/api/report1', methods=['POST'])
def energyConsumedOverPeriod():
    new_item = request.json
    fromDate = new_item['fromDate']
    toDate = new_item['toDate']

    smartmeter_data = SmartMeterServices()
    data = smartmeter_data.getConsolidatedData(fromDate, toDate)  ## str: value
    return jsonify({"message": str(data)}), 200


@app.route('/api/report1/extended', methods=['POST'])
def energyConsumedOverPeriod_Extended():
    new_item = request.json
    fromDate = new_item['fromDate']
    toDate = new_item['toDate']

    smartmeter_data = SmartMeterServices()
    data = smartmeter_data.getConsolidatedFullData(fromDate, toDate)  ## str: value
    return jsonify({"message": data}), 200


@app.route('/api/report1/bymeterid', methods=['POST'])
def energyConsumedOverPeriod_ByMeterId():
    new_item = request.json
    fromDate = new_item['fromDate']
    toDate = new_item['toDate']
    meterId = new_item['meterId']

    smartmeter_data = SmartMeterServices()
    data = smartmeter_data.getConsolidatedFullDataByMeterId(meterId, fromDate, toDate)  ## str: value
    return jsonify({"message": data}), 200


"""
    # AWATTAR LIVE AND PREDICTED PRICE
    The following methods are used to retrieve the data from AWATTAR SERVICES
"""


# Report 4 - Average Awattar price over period
@app.route('/api/report4', methods=['POST'])
def averageAwattarPriceOverPeriod():
    new_item = request.json
    fromDate = new_item['fromDate']
    toDate = new_item['toDate']
    get_avg_data = AwattarServices()
    data = get_avg_data.get_average_awattar_price_over_period(fromDate, toDate)
    return jsonify({"message": str(data)}), 200


"""
    Get all 5 reports based on the start-date and end-date
    Smart-meter services:  requires only start and end date
    Awattar services: requires both date and time
    
    Formula:
    R1 = Get the data from the Smart-Meter Json api
    R2 = R1 x R4
    R3 = R2 / R1
    R4 = Get the data from Awattar services and Consolidate it
    R5 = R2 - R1 x R4

"""


# All 5 reports
@app.route('/api/getAllReports', methods=['POST'])
def getAllReports():
    new_item = request.json
    fromDate_sm = new_item['fromDate_sm']
    toDate_sm = new_item['toDate_sm']
    fromDate_aws = new_item['fromDate_aws']
    toDate_aws = new_item['toDate_aws']

    # Get R1 and R4 values
    smartmeter_data = SmartMeterServices()
    R1 = smartmeter_data.getConsolidatedData(fromDate_sm, toDate_sm)  ## str: value

    get_avg_data = AwattarServices()
    R4 = get_avg_data.get_average_awattar_price_over_period(fromDate_aws, toDate_aws)

    print(R1)  # smart meter info are in kWh

    # awattar prices are in Mwh, so we need to convert this values
    print(R4 * 1000)  # mwh to kwh = multiply the energy value by 1000

    # Calculate R2 and R3
    R2 = R1 * R4
    R3 = R2 / R1
    R5 = R2 - (R1 * R4)

    all_reports = {"report1": str(R1),
                   "report2": str(R2),
                   "report3": str(R3),
                   "report4": str(R4),
                   "report5": str(R5)}
    return jsonify({"message": str(all_reports)}), 200


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
    #    app.run(debug=True)
    custom_ip = '192.168.1.166'
    custom_port = 8080
    app.run(host=custom_ip, port=custom_port, debug=True)
    download_awattar_data = AwattarServices().download_awattar_data()

    # Run the scheduler loop in a separate thread
    while True:
        schedule.run_pending()
        time.sleep(1)
