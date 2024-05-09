
class Client:

    def __init__(self):
        self._token = None
        self._chat_room_name = None
        self._chat_room_password = None
        self._user_name = None


    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        if self._user_name is None:
            self._user_name = user_name

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        if self._token is None:
            self._token = token

    @property
    def chat_room_name(self):
        return self._chat_room_name

    @chat_room_name.setter
    def chat_room_name(self, chat_room_name):
        if self._chat_room_name is None:
            self._chat_room_name = chat_room_name
