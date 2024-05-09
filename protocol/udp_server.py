from super_protocol import BaseUDP

class UDPServer(BaseUDP):
    def __init__(self):
        super().__init__()
        self.socket.bind((self.server_address, self.server_port))
        print(f"UDP Server listening on {self.server_address}:{self.server_port}")

    def run(self):
        while True:
            data_dict, address = self.receive_data()
            print(f"Received data from {address}: {data_dict}")
            self.send_data(address, {'response': 'Message received'})


