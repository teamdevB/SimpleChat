from super_protocol import BaseSocket
import socket

class TCPClient(BaseSocket):
    def __init__(self):
        super().__init__()
        if self.connect():
            print(f"{self.server_address}:{self.server_port}に接続しました")

    def connect(self):
        try:
            self.socket.connect((self.server_address, self.server_port))
            print("Connected to the server at {}:{}".format(self.server_address, self.server_port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return False  # 返り値で接続の成否を示す
        return True
    
    def receive_message(self):
        try:
            response_bytes = self.socket.recv(self.buffer)
            if len(response_bytes) != 32:  # header+bodyは32bytes
                print("Received incomplete data.")
                return None
            return self.header_and_body_to_dict(response_bytes)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            self.close_connection()
            return None

if __name__ == "__main__":
    client = TCPClient()
    dic = {
        'room_name': "room_name1",
        'operation': 0,
        'state': 0,
        'username': "username1",
        'password': "password1",
        'token': "token1"
    }
    client.send_request(dic)