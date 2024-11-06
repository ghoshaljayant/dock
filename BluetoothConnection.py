import threading
import bluetooth

from Connection import ConnectionInterface


class BluetoothConnection(ConnectionInterface):

    def __init__(self, server_address:str, port:int):
        self.server_address = server_address
        self.port = port
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def initialize(self):
        try:
            self.sock.connect((self.server_address, self.port))
            #self.listen_for_data()
        except bluetooth.BluetoothError as e:
            print(f"Failed to connect: {e}")
        return "Initial function executed on page load."
        pass

    # Helper function to send data in a separate thread
    def send_in_thread(self, message):
        def send():
            try:
                self.sock.send(message)
                print(f"Message '{message}' sent successfully!")
            except bluetooth.BluetoothError as e:
                print(f"Error sending message '{message}': {e}")

        thread = threading.Thread(target=send)
        thread.start()
        return thread

    # Start a thread to continuously listen for data
    def listen_for_data(self):
        def listen():
            try:
                while True:
                    data = self.sock.recv(1024)  # Receive up to 1024 bytes
                    if data:
                        print(f"Received data: {data.decode('utf-8')}")
            except bluetooth.BluetoothError as e:
                print(f"Error receiving data: {e}")

        thread = threading.Thread(target=listen, daemon=True)  # Daemon thread to keep listening
        thread.start()

    def send(self, value:str):
        self.send_in_thread(value)
        pass

    def onReceive(self,value:str):
        pass