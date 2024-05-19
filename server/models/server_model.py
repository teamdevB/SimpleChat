# from chat_room_list import ChatRoomList
# from chat_room import ChatRoom
# from user import User
from protocol.tcp_server import TCPServer
# from protocol.udp_protocol import UDPServer
import configparser
from server.views.server_view import ServerView


# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read('./settings/config.ini', encoding='utf-8')

HOST = config['SERVER']['Host']
PORT = int(config['SERVER']['Port'])
MAX_CLIENTS = int(config['SERVER']['MaxClients'])
BASE_DIR_TEMPLATE = config['SERVER']['Base_Dir_Templates']

class ServerModel:
    def __init__(self):
        super().__init__()
        self.clients = {}
        self.tokens = {}
        self.tcp = None
        self.view = ServerView(BASE_DIR_TEMPLATE)

    # def start_server(self):
    #     self.start()
    #     self.run()

    def setup(self):
        # Serverの立ち上げ
        if self.tcp is None:
            self.tcp = TCPServer(HOST, PORT, MAX_CLIENTS)

    def tcp_accept(self):
        connection, address = self.tcp.accept()

        print(self.view.template('tcp_accept_1.txt').substitute({
            'address': address
        }))

        return connection, address
    #
    #
    #
    #def tcp_handler(self):
    #     ## 受信
    #     user_name  = response_dict["user_name"]
    #     user = User(udp_addr=None, tcp_addr=None,  response_dict["user_name"],is_host = False)
    #     self.clients[user_name] = user
    #     self.tokens[user_name] = user.join_token
    #
    #     room_name = response_dict["room_name"]
    #     if not self.check_roomname(room_name):
    #         self.add_room(room_name)
    #         self.set_password(response_dict["password"])
    #         user.is_host = True
    #         self.get_room(room_name).add_client_info(user)
    #         print(f"{user_name}が{room_name}に参加しました")
    #     else:
    #         if not self.get_room(room_name).is_password_checked(response_dict["password"]):
    #             print("パスワードが違います")
    #         else:
    #             self.get_room(room_name).add_client_info(user)
    #             print(f"{user_name}が{room_name}に参加しました")
    #
    #
    # def udp_handler(self):
    #     room_name = response_dict["room_name"]
    #     message = response_dict["message"]
    #     for client in self.get_room(room_name).client_infos:
    #         self.send_data(client.udp_addr, message)
