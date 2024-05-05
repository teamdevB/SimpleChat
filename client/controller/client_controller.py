import threading
import socket as soc
from client.models.client_model import ClientModel

class ClientController:

    def __init__(self):
        self.socket = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        user_name = input("ユーザー名を入力してください: ")

        # User_name Tokenを登録する処理
        self.client_model = ClientModel(user_name, 'token')

    def receive_messages(self):
        while True:
            data, _ = self.socket.recvfrom(4096)
            # username_len = data[0]
            # username = data[1:username_len + 1].decode('utf-8')
            # message = data[username_len + 1:].decode('utf-8')
            # print(f"{username}: {message}")



    def send_messages(self):
        while True:
            message = input()
            if message == 'view':
                print(self.client_model.get_token())
                continue

            # username_bytes = cls.username.encode('utf-8')
            # message_bytes = message.encode('utf-8')
            print(f'replay {message}')

            # data = bytes([len(username_bytes)]) + username_bytes + message_bytes
            # self.socket.sendto(data, (SERVER_HOST, SERVER_PORT))


    def start(self):
        print('Chatを開始します')

        # TCRP(チャットルームを作成する、チャットルームに参加する、)

        # UDP(メッセージのやり取り)
        received_message_thread = threading.Thread(target=self.receive_messages)
        send_message_thread = threading.Thread(target=self.send_messages)

        received_message_thread.start()
        send_message_thread.start()

        received_message_thread.join()
        send_message_thread.join()
