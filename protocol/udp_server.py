from super_protocol import BaseUDP
import json

class UDPServer(BaseUDP):
    def __init__(self):
        super().__init__()
        self.socket.bind((self.server_address, self.server_port))
        print(f"UDP Server listening on {self.server_address}:{self.server_port}")
