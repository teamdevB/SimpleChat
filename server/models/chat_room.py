
class ChatRoom():
    def __init__(self, room_name):
        self.room_name = room_name
        self.client_infos = []
        self.password = None
    def set_password(self, password):
        self.password = password
    def is_password_checked(self, password):
        return self.password == password
    def add_client_info(self, client_info):
        if client_info not in self.client_infos:
            self.client_infos.append(client_info)
    def remove_client_info(self, client_info):
        self.client_infos.remove(client_info)

    
