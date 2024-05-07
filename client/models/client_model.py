from client.models.client import Client
from client.views.client_view import ClientView

class ClientModel:
    def __init__(self):
        self.client = None

    def __set_user_name(self, user_name):
        if self.client is None:
            self.client = Client(user_name)

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

    def create_chat_room_prompt(self):
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
