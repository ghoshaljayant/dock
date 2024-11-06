import bluetooth
import subprocess
import threading
from JsonHelper import read_json_file

json_dict=read_json_file("./config.json")
button_configs=json_dict["dock_config"]["buttons_config"]

def get_json_value(keys):
    data=json_dict   
    for i in keys:
        data = data[i]
    print(data)
    return data



def run_commands(index):
    action = ['code']
    button_config = button_configs[int(index)-1]
    action = (button_config["command"])
    # Run the subprocess in a separate thread
    thread = threading.Thread(target=subprocess.run, args=(action,), kwargs={'capture_output': True, 'text': True})
    thread.start()
    


def init_recv(server_sock, port):    
    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Waiting for connection...")

    # Accept a connection from the Pi
    client_sock, address = server_sock.accept()
    print(f"Accepted connection from {address}")
    try:
        while True:
            # Receive message with a buffer size of 1024 bytes
            data = client_sock.recv(1024)  # Adjust buffer size as needed
            if not data:
                # If no data is received, break the loop (connection closed)
                print("Connection closed by the client.")
                break

            # Decode and print the message
            message = data.decode()
            print("Received message:", message)
            run_commands(message)
        

    finally:
        # Close the connection
        client_sock.close()
        server_sock.close()
        print("Server closed.")
        init_recv(bluetooth.BluetoothSocket(bluetooth.RFCOMM),port)

# Set up the Bluetooth server socket
port = 1
init_recv(bluetooth.BluetoothSocket(bluetooth.RFCOMM),port)



