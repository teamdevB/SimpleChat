from .super_protocol import BaseSocket
import socket

class TCPServer(BaseSocket):
    def __init__(self):
        super().__init__()
        self.socket.bind((self.server_address, self.server_port))
        self.socket.listen(5)

    def accept_connection(self):
        try:
            self.connection, self.client_address = self.socket.accept()
            print(f"{self.client_address}からの接続を受け入れました")
            return True
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.close_connection()  # エラー発生時に接続を閉じる
            return False
        
    def send_request(self, received_dict):
        self.dict_to_bytes(received_dict)
        print(f"Sending: {self.header + self.body}")  # 送信データのログ
        print(f"Header: {self.header}, Body: {self.body}")
        try:
            self.connection.sendall(self.header + self.body)
        except socket.error as e:
            print("ここでエラー")
            print(f"Error sending data: {e}")
            self.close_connection()
            return False
        return True

    def receive_message(self):
        try:
            response_bytes = self.connection.recv(self.buffer)
            if len(response_bytes) != 32:  # header+bodyは32bytes
                print("Received incomplete data.")
                return None
            return self.header_and_body_to_dict(response_bytes)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            self.close_connection()
            return None



    def connect(self):
        try:
            self.socket.connect((self.server_address, self.server_port))
            print("Connected to the server at {}:{}".format(self.server_address, self.server_port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return False  # 返り値で接続の成否を示す
        return True



    def dict_to_bytes(self, dict):
        self.room_name = dict['room_name'].encode('utf-8').ljust(8, b'\x00')
        self.operation = dict['operation'].to_bytes(1, 'big')
        self.state = dict['state'].to_bytes(1, 'big')
        self.user_name = dict['username'].encode('utf-8').ljust(5, b'\x00')
        self.password = dict['password'].encode('utf-8').ljust(8, b'\x00')
        self.token = dict['token'].encode('utf-8').ljust(8, b'\x00')
        self.set_head_and_body()
