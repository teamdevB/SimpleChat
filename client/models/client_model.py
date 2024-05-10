from client.models.client import Client
from client.views.client_view import ClientView
from protocol.tcp_client import TCPClient

class ClientModel:
    def __init__(self):
        self.client = Client()
        self.tcp = TCPClient()

    def __set_user_name(self, user_name):
        self.client.user_name = user_name

    def __set_chat_room_name(self, chat_room_name):
        self.client.chat_room_name = chat_room_name


    def get_user_name(self):
        return self.client.user_name

    def get_token(self):
        return self.client.__token

    def __continue(self):
        template = ClientView.get_template('continue.txt')
        print(template.substitute())

    def ask_user_name(self):
        template = ClientView.get_template('ask_for_username.txt')
        user_name = input(template.substitute())
        self.__set_user_name(user_name)

    def ask_server_info(self):
        template = ClientView.get_template('ask_for_server_info_1.txt')
        server_address = input(template.substitute())

        template = ClientView.get_template('ask_for_server_info_2.txt')
        server_port = input(template.substitute())

        template = ClientView.get_template('ask_for_server_info_3.txt')
        print(template.substitute({
            'server_host': server_address,
            'server_port': server_port
        }))

        if server_port == '':
            server_port = 9001

        self.tcp.server_address = server_address
        self.tcp.server_port    = int(server_port)

    def create_chat_room_or_join_prompt(self):
        while True:
            template = ClientView.get_template('ask_for_operation.txt')
            operation = int(input(template.substitute({
                'user_name': self.get_user_name()
            })))
            if operation == 1:
                return True
            elif operation == 2:
                return False
            else:
                self.__continue()

    def create_chat_room(self):
        while True:
            # chat_room_name
            template = ClientView.get_template('ask_for_create_chat_room_1.txt')
            chat_room_name = input(template.substitute())

            # chat_room_password
            template = ClientView.get_template('ask_for_create_chat_room_2.txt')
            chat_room_password = input(template.substitute({
                'chat_room_name': chat_room_name
            }))

            # check
            template = ClientView.get_template('ask_for_create_chat_room_3.txt')
            is_y = input(template.substitute({
                'chat_room_name': chat_room_name,
                'chat_room_password': chat_room_password
            }))

            if is_y == 'y':
                break
            self.__continue()
