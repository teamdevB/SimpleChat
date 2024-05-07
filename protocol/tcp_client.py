import socket

class TCPClient():
    def __init__(self):
        self.server_address = 'localhost'
        self.server_port = 9001
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 32

    def connect(self):
        self.socket.connect((self.server_address, self.server_port))
        print("Connected to the server at {}:{}".format(self.server_address, self.server_port))
    
    def send_header(self, room_name_size, operation, state, room_name, user_name, password):
        room_name_encode = self.ljust_replace_space(room_name, 8)
        user_name_encode = self.ljust_replace_space(user_name, 10)
        password_encode = self.ljust_replace_space(password, 11)
        
        header = room_name_size.to_bytes(1, 'big') + \
            operation.to_bytes(1, 'big') + \
            state.to_bytes(1, 'big') + \
            room_name_encode + \
            user_name_encode + \
            password_encode

        self.socket.send(header)
        print("Header sent to server.")
    
    @staticmethod
    def ljust_replace_space(original_str: str, num: int) -> bytes:
        byte_str = original_str.encode('utf-8')
        if len(byte_str) < num:
            return byte_str.ljust(num, b' ')
        else:
            return byte_str[:num]
    
    def receive_message(self):
        message = self.socket.recv(self.buffer)
        return message.decode('utf-8')
    
    def close_connection(self):
        self.socket.close()
        print("Connection closed.")

# 使用例
if __name__ == "__main__":
    client = TCPClient()
    client.connect()
    client.send_header(0x01, 0x01, 0x01, "Room1", "user123", "pass123")
    response = client.receive_message()
    print("Received from server:", response)
    client.close_connection()
