import threading
import socket as soc
from client.models.client_model import ClientModel
from client.views.client_view import ClientView

class ClientController:

    def __init__(self):
        self.client_model = ClientModel()

    def start(self):

        # server情報
        self.client_model.ask_server_info()

        # 接続確認
        self.client_model.tcp.connect()

        # ユーザー名の入力
        self.client_model.ask_user_name()

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
        message = self.client_model.tcp.receive_message()
        print("serverからのmessage: ", message)
        if message["state"] == 1:
            parameter = self.client_model.generate_request_params(state=2)
            self.client_model.tcp.send_request(parameter)

        send_message_thread = threading.Thread(target=self.client_model.udp.send_message(self.client_model.client.chat_room_name, self.client_model.client.token))
        received_message_thread = threading.Thread(target=self.client_model.udp.listen_for_responses())

        received_message_thread.start()
        send_message_thread.start()

        # received_message_thread.join()
        # send_message_thread.join()
