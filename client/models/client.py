
class Client:

    def __init__(self, user_name):
        self.__token = None
        self.__user_name = user_name

    @property
    def user_name(self):
        return self.__user_name

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token
