import json
from flask import Flask, render_template, request, jsonify
from BluetoothConnection import BluetoothConnection
from Connection import ConnectionInterface

app = Flask(__name__)

# Read and parse JSON file for configuration
def read_json_file(json_path):
    try:
        with open(json_path, 'r', encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(e)

json_dict = read_json_file("./config.json")

group_config_dict = json_dict["dock_config"]["group_config"]
group_length = len(group_config_dict)

buttons_config = json_dict["dock_config"]["buttons_config"]

buttons_group = dict()

for group_key in group_config_dict.keys():
    buttons_group[group_key]=list()

for button in buttons_config:
    buttons_group[button["group_index"]].append(button)

print(buttons_group["1"])


server_address = str(json_dict["dock_config"]["device_config"]["address"])
port = int(json_dict["dock_config"]["device_config"]["port"])

# TODO here we need a factory method
connection: ConnectionInterface = BluetoothConnection(server_address, port)

# Function that runs when the page loads
def run_on_page_load():    
    connection.initialize()
    return "Initial function executed on page load."

# Function to trigger each button's action
def function_action(index):
    print(index)
    connection.send(index)
    return f"Function {index} Executed!"

# Route for the homepage
@app.route('/')
def index():
    run_on_page_load()
    return render_template('index.html', buttons_config=buttons_config,buttons_group=buttons_group, group_config=group_config_dict)

# Route to handle button press and run corresponding function
@app.route('/run-function', methods=['POST'])
def run_function():
    data = request.get_json()
    function_key = data.get('function')
    if function_key:
        result = function_action(function_key)
        print(result)  # For debugging/logging purposes
    else:
        result = "Invalid Function"

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
