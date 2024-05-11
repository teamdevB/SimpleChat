from .super_protocol import BaseSocket
import socket
import threading

class TCPServer(BaseSocket):
    def __init__(self):
        super().__init__()
        self.socket.bind((self.server_address, self.server_port))
        self.socket.listen(5)

    def start_server(self):
        while True:
            client_connecton, client_address = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_connecton, client_address))
            client_thread.start()

    def handle_client(self, connection, client_address):
        """ クライアントとの接続を処理するスレッドのターゲット関数です。 """
        try:
            print(f"{client_address}からの接続を受け入れました。")
            while True:
                response_bytes = connection.recv(self.buffer)
                if len(response_bytes) == 0:
                    break  # クライアントが接続を閉じた場合
                if len(response_bytes) != 32:
                    print("Received incomplete data.")
                    continue
                received_dict = self.header_and_body_to_dict(response_bytes)
                print(f"{received_dict['user_name']}から受取ったdict: \n", received_dict)
                received_dict["room_name"] = "ctake"
                received_dict["operation"] = 12
                print(f"{received_dict['user_name']}ヘ送ったdict : \n", received_dict)
                self.send_request(received_dict, connection)
        except socket.error as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            connection.close()
            print(f"Connection with {client_address} has been closed.")
        

    def send_request(self, received_dict, connection):
        """ クライアントへデータを送信 """
        self.dict_to_bytes(received_dict)
        try:
            connection.sendall(self.header + self.body)
        except socket.error as e:
            print(f"Error sending data to {received_dict['username']}: {e}")

    def receive_message(self, connection):
        try:
            response_bytes = connection.recv(self.buffer)
            if len(response_bytes) != 32:  # header+bodyは32bytes
                print("Received incomplete data.")
                return None
            return self.header_and_body_to_dict(response_bytes)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            self.close_connection()
            return None
