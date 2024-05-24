from server.models.chat_room_list import ChatRoomList
from protocol.tcp_server import TCPServer
from protocol.udp_server import UDPServer
import configparser
from server.views.server_view import ServerView
import json
import logging
import uuid
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
        self.udp = None
        self.chat_room_list = ChatRoomList()
        self.view = ServerView(BASE_DIR_TEMPLATE)


    def setup(self):
        # Serverの立ち上げ
        if self.tcp is None:
            self.tcp = TCPServer(HOST, PORT, MAX_CLIENTS)
        if self.udp is None:
            self.udp = UDPServer(HOST, PORT)

    def tcp_accept(self):
        connection, address = self.tcp.accept()

        print(self.view.template('tcp_accept_1.txt').substitute({
            'address': address
        }))

        return connection, address

    def create_or_join_server_room_prompt(self, client_connection):
        try:
            client_request = self.tcp.receive_message(client_connection)
            if client_request['operation'] == 1:
                self.create_room(client_connection, client_request)
            elif client_request['operation'] == 2:
                self.join_room(client_connection, client_request)
            else:
                print("Invalid operation request.")
        except Exception as e:
            print(f"Error handling client request: {e}")

    def create_room(self, client_connection, client_request):
        if not self.chat_room_list.check_room_name(client_request['room_name']):
            self.chat_room_list.add_room(client_request['room_name'])
            self.chat_room_list.set_room_password(client_request["room_name"], client_request["password"])
            chat_room = self.chat_room_list.get_room(client_request['room_name'])
            chat_room.user_list.add_user(client_request['user_name'])
            client_request['state'] = 1
            client_request["password"] = ""
            client_request['token'] = client_request['user_name'] + ":" + self.generate_token()
            self.tcp.send_request(client_connection, client_request)
            client_request = self.tcp.receive_message(client_connection)

    def join_room(self, client_connection, client_request):
        ## ルームが存在するか確認
        if self.chat_room_list.check_room_name(client_request['room_name']) :
            chat_room = self.chat_room_list.get_room(client_request['room_name'])
            # パスワードが一致するか確認
            if chat_room.is_password_checked(client_request["password"]):
                chat_room.user_list.add_user(client_request['user_name'])
                client_request['state'] = 1
                client_request["password"] = ""
                client_request['token'] = client_request['user_name'] + ":" + self.generate_token()
                self.tcp.send_request(client_connection, client_request)
                client_request = self.tcp.receive_message(client_connection)
                
    def start_udp_server(self):
        self.run()
        
    def run(self):
        logging.info("Server is running and waiting for messages...")
        try:
            while True:
                data_bytes, address = self.udp.socket.recvfrom(4096)
                print(data_bytes)
                print(address)
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
            room = self.chat_room_list.get_room(room_name)
            print(room)
            room.add_udp(address)
            print(f"room address list:{room.get_udp_list()}")
            logging.info(f"Received message from {address}: {data_dict}")
            address_list = room.get_udp_list()

            self.broadcast(data_dict, address,address_list )
        except KeyError as e:
            logging.error(f"KeyError: {e} - Possibly malformed message: {data_dict}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
    def broadcast(self, message, sender_address,address_list):
        """受け取ったメッセージを登録されたクライアント全員に送信する（送信者を除く）。"""

        for client_address in address_list:
            if client_address != sender_address:  # 送信者自身には送らない
                data_bytes = json.dumps(message).encode('utf-8')
                print(data_bytes)
                print(client_address)
                self.udp.socket.sendto(data_bytes, client_address)

    def generate_token(self):
        return uuid.uuid4().hex
