from  server.models.chat_room_list import ChatRoomList
from server.models.chat_room import ChatRoom
from server.models.user_list import UserList
from protocol.tcp_server import TCPServer
from protocol.udp_server import UDPServer
import configparser
from server.views.server_view import ServerView
import json
import logging

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

    def start_udp_server(self):
        self.udp = UDPServer(HOST, PORT)
        self.run()
    def run(self):
        logging.info("Server is running and waiting for messages...")
        try:
            while True:
                data_bytes, address = self.udp.socket.recvfrom(4096)
                data_dict = json.loads(data_bytes.decode('utf-8'))
                self.process_message(data_dict, address)
        except KeyboardInterrupt:
            logging.info("Server is shutting down.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            self.udp.socket.close()
    def process_message(self, data_dict, address):
        try:
            room_name = data_dict["room_name"]
            sender_token = data_dict["token"]
            room = self.get_room(room_name)
            room.add_hash_token_udp(sender_token, address)
            room.add_client_token(sender_token)
            logging.info(f"Received message from {address}: {data_dict}")
            token_list = room.get_token_list()
            hash_map_token_udp = room.get_hash_token_udp()
            self.broadcast(data_dict, sender_token, token_list, hash_map_token_udp)
        except KeyError as e:
            logging.error(f"KeyError: {e} - Possibly malformed message: {data_dict}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
    def broadcast(self, message, sender_token,token_list,hash_map_token_udp):
        """受け取ったメッセージを登録されたクライアント全員に送信する（送信者を除く）。"""

        for client_token in token_list:
            if client_token != sender_token:  # 送信者自身には送らない
                data_bytes = json.dumps(message).encode('utf-8')
                self.udp.socket.sendto(data_bytes, hash_map_token_udp[client_token])