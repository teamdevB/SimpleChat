from protocol.super_protocol import BaseUDP

class UDPClient(BaseUDP):
    def __init__(self):
        super().__init__()

    def initial_message(self,room_name,token):
            user_name = token.split(":")[0]
            data_dict = {
                "room_name": room_name,
                "token": token,
                "message": user_name + " has joined the chat."
            }
            self.send_data((self.server_address, self.server_port), data_dict)

    def send_message(self, room_name, token):
        while True:
            message = input()
            data_dict = {
                "room_name": room_name,
                "token": token,
                "message": message
            }
            self.send_data((self.server_address, self.server_port), data_dict)

    def listen_for_responses(self):
        while True:
            response_dict, address = self.receive_data()
            print(f"Response from server {address}: {response_dict}")
