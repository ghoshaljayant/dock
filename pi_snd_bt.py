import bluetooth

is_device_search_enabled=False

if is_device_search_enabled:
    nearby_devices = bluetooth.discover_devices(lookup_names=True,duration=1)
    print(f"Found {len(nearby_devices)} devices.")

    for addr, name in nearby_devices:
        print(f"  {addr} - {name}")
else:
    # Replace with your laptop's Bluetooth address (find it by using `bluetoothctl` or other Bluetooth tools)
    server_address = "60:E3:2B:A3:28:51"

port = 1

# Create a Bluetooth socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_address, port))

try:
    while True:
        # Send a message
        message = input("Enter a message to send: ")
        
        # Check if the user wants to exit
        if message.lower() == "exit":
            print("Exiting...")
            break

        sock.send(message)
        print(f"Message sent: {message}")


finally:
    # Close the connection
    sock.close()

