
class Client:

    def __init__(self):
        self._user_name = None
        self._operation = None
        self._chat_room_name = None
        self._chat_room_password = None
        self._token = None


    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        if self._user_name is None:
            self._user_name = user_name

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, operation):
        if self._operation is None:
            self._operation = operation

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

    @property
    def chat_room_password(self):
        return self._chat_room_password

    @chat_room_password.setter
    def chat_room_password(self, chat_room_password):
        if self._chat_room_password is None:
            self._chat_room_password = chat_room_password
