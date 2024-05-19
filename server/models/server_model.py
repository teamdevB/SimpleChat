from  server.models.chat_room_list import ChatRoomList
# from chat_room import ChatRoom
# from user import User
from protocol.tcp_server import TCPServer
# from protocol.udp_protocol import UDPServer
import configparser
from server.views.server_view import ServerView
import json


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

    def create_or_join_server_room_prompt(self, client_connection):
        ## 受信
        client_request = self.tcp.receive_message(client_connection)
        #self.tcp.send_request(client_connection, client_request)

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

                # self.get_room(room_name).add_client_info(user)
                # print(f"{user_name}が{room_name}に参加しました")

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

        # user_name  = response_dict["user_name"]
        # user = User(udp_addr=None, tcp_addr=None,  response_dict["user_name"],is_host = False)
        # self.clients[user_name] = user
        # self.tokens[user_name] = user.join_token
        #
        # room_name = response_dict["room_name"]
        # if not self.check_roomname(room_name):
        #     self.add_room(room_name)
        #     self.set_password(response_dict["password"])
        #     user.is_host = True
        #     self.get_room(room_name).add_client_info(user)
        #     print(f"{user_name}が{room_name}に参加しました")
        # else:
        #     if not self.get_room(room_name).is_password_checked(response_dict["password"]):
        #         print("パスワードが違います")
        #     else:
        #         self.get_room(room_name).add_client_info(user)
        #         print(f"{user_name}が{room_name}に参加しました")


    # def udp_handler(self):
    #     room_name = response_dict["room_name"]
    #     message = response_dict["message"]
    #     for client in self.get_room(room_name).client_infos:
    #         self.send_data(client.udp_addr, message)
    def run(self):
            print("Server is running and waiting for messages...")
            try:
                while True:
                    data_bytes, address = self.socket.recvfrom(4096)
                    data_dict = json.loads(data_bytes.decode('utf-8'))
                    room_name = data_dict["room_name"]
                    room_client_infos = self.get_room(room_name).get_client_info_udp()
                    room_client_infos.add_client_udp(address)
                    print(f"Received message from {address}: {data_dict}")
                    self.broadcast(data_dict, address,room_client_infos)
            except KeyboardInterrupt:
                print("Server is shutting down.")
            finally:
                self.socket.close()
    def broadcast(self, message, sender_address,room_client_udps):
        """受け取ったメッセージを登録されたクライアント全員に送信する（送信者を除く）。"""

        for client_udp in room_client_udps:
            if client_udp != sender_address:  # 送信者自身には送らない
                data_bytes = json.dumps(message).encode('utf-8')
                self.socket.sendto(data_bytes, client_udp)