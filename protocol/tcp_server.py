from .super_protocol import BaseSocket
from .cliant_handler import ClientHandler
import socket

class TCPServer(BaseSocket):
    def __init__(self):
        super().__init__()

    
import socket
import threading

class TCPServer:
    def __init__(self, host='localhost', port=9001):
        self.server_address = host
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_address, self.server_port))
        self.server_socket.listen(5)
        print(f"サーバーが {self.server_address}:{self.server_port} で起動しました。")

    def start(self):
        try:
            while True:
                print("クライアントからの接続を待っています...")
                connection, address = self.server_socket.accept()
                handler = ClientHandler(connection, address)
                threading.Thread(target=handler.handle_client).start()
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = TCPServer()
    server.start()
