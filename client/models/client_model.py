from client.models.client import Client


class ClientModel:
    def __init__(self, user_name, token):
        print('bbbbbb')
        self.client = Client(user_name, token)

    def get_token(self):
        return self.client.token
