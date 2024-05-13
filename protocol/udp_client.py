from super_protocol import BaseUDP

class UDPClient(BaseUDP):
    def __init__(self):
        super().__init__()

    def send_message(self, room_name, token, message):
        data_dict = {
            'room_name': room_name,
            'token': token,
            'message': message
        }
        self.send_data((self.server_address, self.server_port), data_dict)

    def listen_for_responses(self):
        while True:
            response_dict, address = self.receive_data()
            print(f"Response from server {address}: {response_dict}")

if __name__ == "__main__":
    client = UDPClient()
    client.send_message('ExampleRoom', 'Token123', 'Hello UDP Server!')
    client.listen_for_responses()
