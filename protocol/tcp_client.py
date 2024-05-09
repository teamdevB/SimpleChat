from super_protocol import BaseSocket
import socket

class TCPClient(BaseSocket):
    def __init__(self):
        super().__init__()
        self.connect()

    def connect(self):
        try:
            self.socket.connect((self.server_address, self.server_port))
            print("Connected to the server at {}:{}".format(self.server_address, self.server_port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return False  # 返り値で接続の成否を示す
        return True
