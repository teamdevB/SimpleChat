import threading
import socket as soc
from client.models.client_model import ClientModel
from client.views.client_view import ClientView
from protocol.tcp_client import TCPClient

class ClientController:

    def __init__(self):
        self.client_model = ClientModel()

    def receive_messages(self):
        while True:
            data, _ = self.socket.recvfrom(4096)
            # User_name Tokenを登録する処理
            #self.client_model = ClientModel(user_name, 'token')

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

        # server情報
        self.client_model.ask_server_info()

        # 接続確認
        self.client_model.tcp.connect()

        # ユーザー名の入力
        self.client_model.ask_user_name()


        parameter = {
            'room_name': 'sample',
            'operation': 1,
            'state': 0,
            'user_name': 'usern',
            'password': 'password',
            'token': ''
        }

        #
        # print(self.client_model.tcp.receive_message())

        # TCRP(チャットルームを作成する、チャットルームに参加する、)
        self.client_model.create_chat_room_or_join_prompt()

        if self.client_model.client.operation == 1:
            # chatroomを作成
            self.client_model.create_chat_room()
        else:
            # chatroomに参加する
            self.client_model.join_chat_room()

        parameter = self.client_model.generate_request_params(state=0)
        self.client_model.tcp.send_request(parameter)
        print(self.client_model.tcp.receive_message())
        input()

        raise Exception
        ### ここまで ##



        # server側に現在作成されているルームを表示する

        # UDP(メッセージのやり取り)
        received_message_thread = threading.Thread(target=self.receive_messages)
        send_message_thread = threading.Thread(target=self.send_messages)

        received_message_thread.start()
        send_message_thread.start()

        received_message_thread.join()
        send_message_thread.join()
