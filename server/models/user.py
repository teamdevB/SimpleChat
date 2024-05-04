# from server_token import Token


class User:

    def __init__(self, user_name):
        self.user_name = user_name

    @property
    def user_name(self):
        return self.user_name
