from protocol.super_protocol import BaseUDP

class UDPServer(BaseUDP):
    def __init__(self, server_address, server_port):
        super().__init__(server_address, server_port)
        self.socket.bind((self.server_address, self.server_port))
        print(f"UDP Server listening on {self.server_address}:{self.server_port}")
