from server.models.user_list import UserList


class ChatRoom:
    def __init__(self, room_name):
        self.room_name = room_name
        self.user_list = UserList()
        self.udp_address = set()
        self.room_password = None

    def set_room_password(self, password):
        self.room_password = password

    def is_password_checked(self, password):
        return self.room_password == password

    def add_client_info(self, client_info):
        if client_info not in self.client_infos:
            self.client_infos.append(client_info)

    def remove_client_info(self, client_info):
        self.client_infos.remove(client_info)
