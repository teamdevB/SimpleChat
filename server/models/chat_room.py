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

    def add_udp(self,  udp_addr):
        if udp_addr not in self.address:
            self.address.append(udp_addr)
            
    def get_udp_list(self):
        return self.address
