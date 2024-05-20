from  server.models.chat_room_list import ChatRoomList
# from chat_room import ChatRoom
# from user import User
from protocol.tcp_server import TCPServer
# from protocol.udp_protocol import UDPServer
import configparser
from server.views.server_view import ServerView



# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read('./settings/config.ini', encoding='utf-8')

# 環境変数の設定
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
        self.chat_room_list = ChatRoomList()
        self.view = ServerView(BASE_DIR_TEMPLATE)



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

    def create_or_join_server_room_prompt(self, client_connection):
        ## 受信
        client_request = self.tcp.receive_message(client_connection)

        if client_request['operation'] == 1:
            #create room
            if not self.chat_room_list.check_room_name(client_request['room_name']):
                self.chat_room_list.add_room(client_request['room_name'])

                self.chat_room_list.set_room_password(
                    client_request["room_name"]
                    ,client_request["password"])

                chat_room = self.chat_room_list.get_room(client_request['room_name'])
                chat_room.user_list.add_user(client_request['user_name'])
                print(chat_room.user_list.get_host_user())
                print(chat_room.user_list.get_guest_users())

                client_request['state'] = 1
                self.tcp.send_request(client_connection, client_request)
                client_request = self.tcp.receive_message(client_connection)


        elif client_request['operation'] == 2:
            # join room
            if self.chat_room_list.check_room_name(client_request['room_name']):
                chat_room = self.chat_room_list.get_room(
                    client_request['room_name'])

                chat_room.user_list.add_user(client_request['user_name'])

                print(chat_room.user_list.get_host_user())
                print(chat_room.user_list.get_guest_users())

                client_request['state'] = 1
                self.tcp.send_request(client_connection, client_request)
                client_request = self.tcp.receive_message(client_connection)
        else:
            pass
