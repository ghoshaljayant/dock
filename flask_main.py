from flask import Flask, render_template_string, request, jsonify
import bluetooth
import threading
import json

app = Flask(__name__)

# Read and parse JSON file for configuration
def read_json_file(json_path):
    try:
        with open(json_path, 'r', encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(e)

json_dict = read_json_file("./config.json")

server_address = str(json_dict["dock_config"]["device_config"]["address"])
port = int(json_dict["dock_config"]["device_config"]["port"])

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

buttons_config=json_dict["dock_config"]["buttons_config"]

# Helper function to send data in a separate thread
def send_in_thread(message):
    def send():
        try:
            sock.send(message)
            print(f"Message '{message}' sent successfully!")
        except bluetooth.BluetoothError as e:
            print(f"Error sending message '{message}': {e}")

    thread = threading.Thread(target=send)
    thread.start()
    return thread

# Function that runs when the page loads
def run_on_page_load():    
    try:
        sock.connect((server_address, port))
        print(f"Connected to {server_address} on port {port}")
    except bluetooth.BluetoothError as e:
        print(f"Failed to connect: {e}")
    return "Initial function executed on page load."

# Function to trigger each button's action
def function_action(index):
    print(index)
    send_in_thread(index)
    return f"Function {index} Executed!"

# Route for the homepage
@app.route('/')
def index():
    run_on_page_load()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dynamic Button Triggered Functions</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 20px;
                }
                button {
                    font-size: 20px;
                    font-weight: bold;
                    padding: 15px 30px;
                    margin: 10px;
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: background-color 0.3s, transform 0.3s;
                }
                button:hover {
                    background-color: #0056b3;
                    transform: scale(1.05);
                }
                button:active {
                    background-color: #004085;
                }
            </style>
            <script>
                function sendRequest(buttonValue) {
                    fetch('/run-function', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ function: buttonValue })
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('result').innerText = data.result;
                    })
                    .catch(error => console.error('Error:', error));
                }
            </script>
        </head>
        <body>
            <h1>Choose an Action</h1>
            {% for btn in buttons_config %}
                <button onclick="sendRequest('{{ btn.index }}')">{{ btn.title }}</button>
            {% endfor %}
        </body>
        </html>
    ''', buttons_config=buttons_config)

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
