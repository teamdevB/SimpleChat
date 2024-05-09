from client.models.client import Client
from client.views.client_view import ClientView

class ClientModel:
    def __init__(self):
        self.client = Client()

    def __set_user_name(self, user_name):
        self.client.user_name = user_name

    def __set_chat_room_name(self, chat_room_name):
        self.client.chat_room_name = chat_room_name

    def __set_server_host(self, server_host):
        self.client.server_host = server_host

    def __set_server_port(self, server_port):
        self.client.server_port = server_port

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
        server_host = input(template.substitute())

        template = ClientView.get_template('ask_for_server_info_2.txt')
        server_port = input(template.substitute())

        template = ClientView.get_template('ask_for_server_info_3.txt')
        print(template.substitute({
            'server_host': server_host,
            'server_port': server_port
        }))

        self.__set_server_host(server_host)
        self.__set_server_port(server_port)

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
