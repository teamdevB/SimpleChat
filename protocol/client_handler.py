import socket
from .super_protocol import BaseSocket

class ClientHandler(BaseSocket):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.client_address = address
    

    def handle_client(self):
        try:
            print(f"{self.client_address}からの接続を受け入れました。")
            while True:
                response_bytes = self.connection.recv(self.buffer)
                if len(response_bytes) == 0:
                    break  # クライアントが接続を閉じた場合
                if len(response_bytes) != 707:
                    print("Received incomplete data.")
                    continue
                received_dict = self.header_and_body_to_dict(response_bytes)
                print(f"{received_dict['user_name']}から受取ったdict: \n", received_dict)
                received_dict["room_name"] = "ctake"
                received_dict["operation"] = 12
                print(f"{received_dict['user_name']}ヘ送ったdict : \n", received_dict)
                self.send_request(received_dict)
        except socket.error as e:
            print(f"Error handling client {self.client_address}: {e}")
        finally:
            self.close_connection(self.connection)
            print(f"Connection with {self.client_address} has been closed.")

    def send_request(self, received_dict):
        """ クライアントへデータを送信 """
        self.dict_to_bytes(received_dict)
        try:
            self.connection.sendall(self.header + self.body)
        except socket.error as e:
            print(f"Error sending data to {received_dict['user_name']}: {e}")

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

