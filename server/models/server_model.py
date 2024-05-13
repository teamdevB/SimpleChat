from chat_room_list import ChatRoomList
from chat_room import ChatRoom
from user import User
from protocol.tcp_protocol import TCPServer
from protocol.udp_protocol import UDPServer
import json

class ServerModel(TCPServer, UDPServer, ChatRoomList,ChatRoom):
    def __init__(self):
        super().__init__()
        self.clients = {}
        self.tokens = {}
    def start_server(self):
        self.start()
        self.run()
        
        
    def tcp_handler(self):
        ## 受信
        user_name  = response_dict["user_name"]
        user = User(udp_addr=None, tcp_addr=None,  response_dict["user_name"],is_host = False)
        self.clients[user_name] = user
        self.tokens[user_name] = user.join_token

        room_name = response_dict["room_name"]
        if not self.check_roomname(room_name):
            self.add_room(room_name)
            self.set_password(response_dict["password"])
            user.is_host = True
            self.get_room(room_name).add_client_info(user)
            print(f"{user_name}が{room_name}に参加しました")
        else:
            if not self.get_room(room_name).is_password_checked(response_dict["password"]):
                print("パスワードが違います")
            else:
                self.get_room(room_name).add_client_info(user)
                print(f"{user_name}が{room_name}に参加しました")
        

    def udp_handler(self):
        room_name = response_dict["room_name"]
