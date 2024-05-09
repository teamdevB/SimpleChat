from super_protocol import BaseSocket

class TCPServer(BaseSocket):
    def __init__(self):
        self.socket.bind((self.server_address, self.server_port))
        self.socket.listen(5)


    def accept_connection(self):
        self.connection, self.client_address = self.socket.accept()
        print(f"Connection accepted from {self.client_address}")
        return True