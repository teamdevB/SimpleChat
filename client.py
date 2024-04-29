import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 65432
BUFFER_SIZE = 4096

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.username = input("ユーザー名を入力してください: ")

    def start(self):
        threading.Thread(target=self.receive_messages).start()
        self.send_messages()

    def receive_messages(self):
        while True:
            data, _ = self.socket.recvfrom(BUFFER_SIZE)
            username_len = data[0]
            username = data[1:username_len+1].decode('utf-8')
            message = data[username_len+1:].decode('utf-8')
            print(f"{username}: {message}")

    def send_messages(self):
        while True:
            message = input()
            username_bytes = self.username.encode('utf-8')
            message_bytes = message.encode('utf-8')
            data = bytes([len(username_bytes)]) + username_bytes + message_bytes
            self.socket.sendto(data, (SERVER_HOST, SERVER_PORT))

if __name__ == '__main__':
    client = Client()
    client.start()