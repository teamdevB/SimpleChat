import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 65432
BUFFER_SIZE = 4096
TIMEOUT = 60  # クライアントのタイムアウト時間（秒）

class Client:
    def __init__(self, addr, username):
        self.addr = addr
        self.username = username
        self.last_message_time = time.time()

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SERVER_HOST, SERVER_PORT))
        self.clients = {}

    def start(self):
        print(f"サーバが起動しました ({SERVER_HOST}:{SERVER_PORT})")
        while True:
            data, addr = self.socket.recvfrom(BUFFER_SIZE)
            self.handle_message(data, addr)

    def handle_message(self, data, addr):
        username_len = data[0]
        username = data[1:username_len+1].decode('utf-8')
        message = data[username_len+1:].decode('utf-8')

        if addr not in self.clients:
            self.clients[addr] = Client(addr, username)
        self.clients[addr].last_message_time = time.time()

        print(f"{username}: {message}")
        self.broadcast_message(data)

    def broadcast_message(self, message):
        for client in list(self.clients.values()):
            if time.time() - client.last_message_time > TIMEOUT:
                del self.clients[client.addr]
            else:
                self.socket.sendto(message, client.addr)

if __name__ == '__main__':
    server = Server()
    server.start()


    