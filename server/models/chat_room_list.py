from server.models.chat_room import ChatRoom
class ChatRoomList():
    def __init__(self):
        self.rooms = {}

    def add_room(self, room_name):
        self.rooms[room_name] = ChatRoom(room_name)

    def check_room_name(self, room_name):
        return room_name in self.rooms

    def get_room(self, room_name):
        return self.rooms.get(room_name)

    def set_room_password(self, room_name, password):
        room = self.get_room(room_name)
        room.set_room_password(password)


    def remove_room(self, room_name):
        del self.rooms[room_name] 
