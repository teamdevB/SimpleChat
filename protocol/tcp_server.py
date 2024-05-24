import socket
from protocol.super_protocol import BaseSocket

class TCPServer:
    def __init__(self, host='localhost', port=9001, max_clients=5):
        self.server_address = host
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_address, self.server_port))
        self.server_socket.listen(max_clients)
        self.base_socket = BaseSocket()

    def close(self):
        try:
            self.server_socket.close()
            print("Connection closed")
        except Exception as e:
            print(f"Error closing socket: {e}")

    def accept(self):
        try:
            connection, address = self.server_socket.accept()
            return connection, address
        except Exception as e:
            self.close()

    def receive_message(self, client_connection):
        # メッセージを受け取り、Dictで返却する
        # headを解析して、サーバー側に送信する
        try:
            response_bytes = client_connection.recv(1024)
            # if len(response_bytes) != 32:  # header+bodyは32bytes
                # print("Received incomplete data.")
                # return None
            if response_bytes:
               print(self.base_socket.header_and_body_to_dict(response_bytes))
               return self.base_socket.header_and_body_to_dict(response_bytes)

        except Exception as e:
            self.close()

    def send_request(self, client_connection, parameter: dict):
        self.base_socket.dict_to_bytes(parameter)
        try:
            client_connection.sendall(self.base_socket.header + self.base_socket.body)
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.close_connection()
            return False
