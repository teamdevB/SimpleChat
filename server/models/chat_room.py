from typing import Any
from server.models.user_list import UserList


class ChatRoom:
    def __init__(self, room_name):
        self.room_name = room_name
        self.user_list = UserList()

        self.address = []
        self.room_password = None

    def set_room_password(self, password):
        self.room_password = password

    def is_password_checked(self, password):
        return self.room_password == password

    def add_client_token(self, client_token):
        if client_token not in self.token_list:
            self.token_list.append(client_token)

    def remove_client_info(self, client_info):
        self.client_infos.remove(client_info)

    def add_udp(self,  udp_addr):
        if udp_addr not in self.address:
            self.address.append(udp_addr)
    def get_udp_list(self):
        return self.address
    
    def get_token_list(self):
        return self.token_list
    
    def get_hash_token_udp(self):
        return self.hash_map_token_udp
