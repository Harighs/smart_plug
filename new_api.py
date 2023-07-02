from flask import Flask, jsonify, request
import os
from control import BulbControl
import RPi.GPIO as GPIO
from awattar_service import AwattarService

current_dir = os.getcwd()
print("Current working directory:", current_dir)

app = Flask(__name__)

# Sample data - Replace this with your actual data or database integration
data = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2"},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3"}
]

# Endpoint to get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/api/bulbon', methods=['GET'])
def get_bulbon():
#    with open('smart_plug/control.py') as control:
#        exec(control.read())
    bulb = BulbControl()
    bulb.bulb_on()
    return jsonify("Executed sucessful..")

@app.route('/api/bulboff', methods=['GET'])
def get_bulboff():
    bulb = BulbControl()
    bulb.bulb_off()
    return jsonify("Executed sucessful..")

# According to market price
@app.route('/api/lessthen/<string:eur>', methods=['GET'])
def control_bulb_market(eur):
    bulb = BulbControl()
    market_status = AwattarService()
    market_status.check_market_price(eur)
    return jsonify("Executed sucessful..")


@app.route('/api/socketcontroller/<int:switchNumber>/<int:switchStatus>', methods=['GET'])
def update_socket_controller(switchNumber, switchStatus):
    bulb = BulbControl()
    bulb.socket_controller(switchNumber, switchStatus)
    return jsonify("Executed sucessful..")

    
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

if __name__ == '__main__':
#    app.run(debug=True)
    custom_ip = '192.168.1.166'
    custom_port = 8080
    app.run(host=custom_ip, port=custom_port, debug=True)
