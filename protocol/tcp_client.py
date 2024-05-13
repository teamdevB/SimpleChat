from .super_protocol import BaseSocket
import socket

class TCPClient(BaseSocket):
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.connect():
            print(f"{self.server_address}:{self.server_port}に接続しました")

    def connect(self):
        try:
            self.socket.connect((self.server_address, self.server_port))
            print("Connected to the server at {}:{}".format(self.server_address, self.server_port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return False  # 返り値で接続の成否を示す
        return True
    
    def receive_message(self):
        try:
            response_bytes = self.socket.recv(self.buffer)
            while True:
                if not response_bytes:
                    print("No data received.")
                    return None  # 接続が閉じられたか、データが空であることを示す
                
                if len(response_bytes) != 32:  # header+bodyは32bytesであることを期待
                    print("Received incomplete data.")
                    continue  # 不完全なデータを受信した場合、次のデータを待つ

                # データが適切な場合、ディクショナリに変換して返す
                message_dict = self.header_and_body_to_dict(response_bytes)
                return message_dict

        except socket.error as e:
            print(f"Error receiving data: {e}")
            self.close_connection()
            return None

    def send_request(self, received_dict):
        self.dict_to_bytes(received_dict)
        if self.socket.fileno() == -1:
            print("Socket is already closed.")
            return False
        try:
            self.socket.sendall(self.header + self.body)
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.close_connection()
            return False
        return True
