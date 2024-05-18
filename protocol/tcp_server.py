import socket
from typing import Tuple, Any


class TCPServer:
    def __init__(self, host='localhost', port=9001, max_clients=5):
        self.server_address = host
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_address, self.server_port))
        self.server_socket.listen(max_clients)

    # Accept
    def accept(self) -> tuple[socket, Any]:
        try:
            connection, address = self.server_socket.accept()
            return connection, address
        finally:
            self.server_socket.close()

    def received(self):
        # メッセージを受け取り、Dictで返却する
        # headを解析して、サーバー側に送信する
        pass
