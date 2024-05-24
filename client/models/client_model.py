from client.models.client import Client
from client.views.client_view import ClientView
from protocol.tcp_client import TCPClient
from protocol.udp_client import UDPClient
import configparser


# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read('./settings/config.ini', encoding='utf-8')

BASE_DIR_TEMPLATE = config['CLIENT']['Base_Dir_Templates']

class ClientModel:
    def __init__(self):
        self.client = Client()
        self.tcp = TCPClient()
        self.udp = UDPClient()
        self.view = ClientView(BASE_DIR_TEMPLATE)

    def generate_request_params(self, state, token=''):
        parameter = {
            'user_name': self.client.user_name,
            'room_name': self.client.chat_room_name,
            'password': self.client.chat_room_password,
            'operation': self.client.operation,
            'state': state,
            'token': token
        }
        return parameter

    def get_user_name(self):
        return self.client.user_name

    def get_token(self):
        return self.client.token

    def set_token(self, token):
        if self.client.token is None:
            self.client.token = token

    def __continue(self):
        template = ClientView.get_template('continue.txt')
        print(template.substitute())

    def ask_user_name(self):

        user_name = input(self.view.template('ask_for_username.txt')
                               .substitute())

        self.client.user_name = user_name

    def ask_server_info(self):

        server_address = input(self.view.template('ask_for_server_info_1.txt')
                               .substitute())

        server_port = input(self.view.template('ask_for_server_info_2.txt')
                            .substitute())

        print(self.view.template('ask_for_server_info_3.txt').substitute({
            'server_host': server_address,
            'server_port': server_port
        }))

        if server_port == '':
            server_port = 9001

        self.tcp.server_address = server_address
        self.tcp.server_port = int(server_port)

    def create_chat_room_or_join_prompt(self):
        while True:
            operation = int(input(self.view.template('ask_for_operation.txt').substitute({
                'user_name': self.get_user_name()
            })))

            if operation == 1 or operation == 2:
                self.client.operation = operation
                break
            else:
                self.__continue()

    def create_chat_room(self):
        while True:
            # chat_room_name
            chat_room_name = input(
                self.view.template('ask_for_create_chat_room_1.txt').substitute())

            # chat_room_password
            chat_room_password = input(
                self.view.template('ask_for_create_chat_room_2.txt').substitute({
                    'chat_room_name': chat_room_name
                }))


            # check
            is_y = input(
                self.view.template('ask_for_create_chat_room_3.txt').substitute({
                        'chat_room_name': chat_room_name,
                        'chat_room_password': chat_room_password
                    }))

            if is_y == 'y':
                self.client.chat_room_name = chat_room_name
                self.client.chat_room_password = chat_room_password
                break
            self.__continue()

    def join_chat_room(self):
        while True:
            print('chat room join')
            # chat_room_name
            chat_room_name = input(
                self.view.template('ask_for_create_chat_room_1.txt').substitute())

            # chat_room_password
            chat_room_password = input(
                self.view.template('ask_for_create_chat_room_2.txt').substitute({
                    'chat_room_name': chat_room_name
                }))


            # check
            is_y = input(
                self.view.template('ask_for_create_chat_room_3.txt').substitute({
                        'chat_room_name': chat_room_name,
                        'chat_room_password': chat_room_password
                    }))

            if is_y == 'y':
                self.client.chat_room_name = chat_room_name
                self.client.chat_room_password = chat_room_password
                break
            self.__continue()
