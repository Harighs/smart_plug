import os

from flask import Flask, jsonify, request

from backend_services import AwattarService
from raspberrypi_controller import RelayControl, enable_relay1, disable_relay1, relay_switch_controller
from smartmeter_services import SmartMeter


current_dir = os.getcwd()
print("Current working directory:", current_dir)

app = Flask(__name__)

# Sample data - Replace this with your actual data or database integration
data = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2"},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3"}
]

########### TESTING ############
@app.route('/api/', methods=['GET'])
def rest_api():
    return jsonify("You're accessing the Enermizer API Services.")

########### REPORT - 1 ############
## Report 1 - Energy consumed over selected time period
@app.route('/api/report1', methods=['POST'])
def energyConsumedOverPeriod():
    smartmeter_data = SmartMeter()
    if smartmeter_data.get_data():
        data = 5555
    
    # data = data['meteredValues'].sum() # --> float
    
    # # assign globe variable
    # global report1
    # report1 = data
    return jsonify({"status": "true"})

    # return jsonify({f"message": str{data}}), 200




# Endpoint to get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)


# TODO Exception handling
@app.route('/api/bulbon', methods=['GET'])
def get_bulbon():
    #    with open('smart_plug/raspberrypi_controller.py') as control:
    #        exec(control.read())
    RelayControl().__init__()
    enable_relay1()
    return jsonify({"status": "true"})


@app.route('/api/bulboff', methods=['GET'])
def get_bulboff():
    RelayControl().__init__()
    disable_relay1()
    return jsonify({"status": "true"})


# According to market price
@app.route('/api/lessthen/<string:eur>', methods=['GET'])
def control_bulb_market(eur):
    RelayControl().__init__()
    market_status = AwattarService()
    market_status.check_market_price(eur)
    return jsonify({"status": "true"})

# Update Market data
@app.route('/api/update_market_data', methods=['GET'])
def update_market_data():
    RelayControl().__init__()
    market_status = AwattarService().update_marketdata()
    return True


# Udate Smart Meter data
@app.route('/api/update_smart_meter_data', methods=['GET'])
def update_smart_meter_data():
    smart_meter = SmartMeter()
    today_data = smart_meter.smart_meter_data # Its a dataframe
    return today_data

@app.route('/api/socketcontroller/<int:switchNumber>/<int:switchStatus>', methods=['GET'])
def update_socket_controller(switchNumber, switchStatus):
    RelayControl().__init__()
    relay_switch_controller(switchNumber, switchStatus)
    return jsonify({"status": "true"})


# Endpoint to get a specific item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404


# Endpoint to add a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item['id'] = len(data) + 1
    data.append(new_item)
    return jsonify(new_item), 201


# Endpoint to update an existing item by ID
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        item.update(request.json)
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404


# Endpoint to delete an item by ID
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({"message": "Item deleted successfully"}), 200


## Test Report - test report
@app.route('/api/test', methods=['GET'])
def api_test():    
    return jsonify({"message", 'sucess'}), 200



    

## Report 2 - Costs of energy consumed = Sum of all hourly Energy consumed x Awattar price
@app.route('/api/report2', methods=['GET'])
def costsOfEnergyConsumed():
    # TODO
    """
    R2 = R1 x R4
    # find the unit of R2
    """
    R1, R4 = get_r1_and_r4_value(fromDate, toDate)
    # assign globe variable
    global report2
    report2 = R1*R4
    return jsonify({"message", report2}), 200


## Report 3 - Average effective price = Costs of energy consumed over period divided by Energy consumed over period
@app.route('/api/report3', methods=['GET'])
def averageEffectivePrice():
    # TODO
    """
    R3 = R2/R1
    # find the unit of R3
    
    """
    global report3
    report3 = report2 / report1
    return jsonify({"message", report3}), 200


## Report 4 - Average Awattar price over period
@app.route('/api/report4/<string:fromDate>/<string:toDate>', methods=['POST'])
def averageAwattarPriceOverPeriod(fromDate, toDate):
    global report4
    
    report4 = get_average_awattar_price_over_period(fromDate, toDate)
    return jsonify({"message", report4}), 200

# ## Report 5 - Savings = Costs of energy consumed minus Sum of all hourly Energy consumed x Average Awattar price
# @app.route('/api/report5/<string:fromDate>/<string:toDate>', methods=['POST'])
# def averageAwattarPriceOverPeriod(fromDate, toDate):
#     """
#     R5 = R2 - R1 x R4
#     """
#     global report5
#     report5 = report2 - report1 * report4
#     return jsonify({"message", report5}), 200

def get_r1_and_r4_value(fromDate, toDate):
    # get R1 value
    smartmeter_data = SmartMeter()
    data = smartmeter_data.SMART_METER_DATA #DF
    R1 = data['meteredValues'].sum() # --> float
    
    # get R4 value
    R4 = get_average_awattar_price_over_period(fromDate, toDate)
    
    return R1, R4

def global_api():
    
    return jsonify({"message", report5}), 200

if __name__ == '__main__':
    #    app.run(debug=True)
    custom_ip = '192.168.1.166'
    custom_port = 8080
    app.run(host=custom_ip, port=custom_port, debug=True)
