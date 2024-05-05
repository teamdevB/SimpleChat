
class Client:

    def __init__(self, user_name, token):
        self._user_name = user_name
        self._token = token

    @property
    def user_name(self):
        return self._user_name

    @property
    def token(self):
        return self._token
