
class Client:

    def __init__(self):
        self._token = None
        self._chat_room_name = None
        self._chat_room_password = None
        self._user_name = None
        self._server_host = None
        self._server_port = None

    @property
    def server_host(self):
        return self._server_host

    @server_host.setter
    def server_host(self, server_host):
        if self._server_host is None:
            self._server_host = server_host
        elif self._server_host == '':
            self._server_host = 'localhost'

    @property
    def server_port(self):
        return self._server_port

    @server_port.setter
    def server_port(self, server_port):
        if self._server_port is None:
            self._server_port = server_port

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
