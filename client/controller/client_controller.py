import threading
from client.models.client_model import ClientModel


class ClientController:

    def __init__(self):
        self.client_model = ClientModel()

    def client_udp_send_handler(self):
        client = self.client_model.client
        print(client.token)
        self.client_model.udp.send_message(
            client.chat_room_name, client.token)

    def client_udp_received_handler(self):
        self.client_model.udp.listen_for_responses()

    def start(self):

        # server情報
        self.client_model.ask_server_info()

        # 接続確認
        self.client_model.tcp.connect()

        # ユーザー名の入力
        self.client_model.ask_user_name()

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

        # server側のトークンを登録する
        self.client_model.client.token = message['token']

        if message["state"] == 1:
            parameter = self.client_model.generate_request_params(state=2)
            self.client_model.tcp.send_request(parameter)

        send_message_thread = threading.Thread(
            target=self.client_udp_send_handler())
        received_message_thread = threading.Thread(
            target=self.client_udp_received_handler())

        received_message_thread.start()
        send_message_thread.start()

        received_message_thread.join()
        send_message_thread.join()
