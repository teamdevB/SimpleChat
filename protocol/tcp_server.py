import socket

class TCPServer():
    def __init__(self):
        self.tcp_header = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = 9001
        self.server_address ='localhost'
        self.buffer = 32
        self.client_address = 0


    def set_header(self, header):
        self.tcp_header = header
        self.room_name_size = self.get_room_name_size()
        self.operation = self.get_operation()
        self.state = self.get_state()
        self.room_name = self.get_room_name()
        self.user_name = self.get_user_name()
        self.password = self.get_password()

    def get_header(self, room_name_size, operation, state, room_name, user_name, password):
        room_name_encode = self.ljust_replace_space(room_name, 8)
        user_name_encode = self.ljust_replace_space(user_name, 10)
        password_encode = self.ljust_replace_space(password, 11)

        return room_name_size.to_bytes(1, 'big') + \
            operation.to_bytes(1, 'big') + \
            state.to_bytes(1, 'big') + \
            room_name_encode + \
            user_name_encode + \
            password_encode
    
    @staticmethod
    def ljust_replace_space(original_str: str, num: int) -> bytes:
        byte_str = original_str.encode('utf-8')
        if len(byte_str) < num:
            return byte_str.ljust(num, b' ')
        else:
            # 長すぎる場合は切り捨てる
            # エラーハンドリングはどこでやる？
            return byte_str[:num] 
    
        
    def get_room_name_size(self):
        return self.tcp_header[0]

    def get_operation(self):
        return self.tcp_header[1]

    def get_state(self):
        return self.tcp_header[2]

    def get_room_name(self):
        return self.tcp_header[3:11].decode('utf-8').replace(' ','')

    def get_user_name(self):
        return self.tcp_header[11:21].decode('utf-8').replace(' ','')

    def get_password(self):
        return self.tcp_header[21:].decode('utf-8').replace(' ','')
    
    def bind(self):
        self.socket.bind((self.server_address, self.server_port))

    def listen(self, total_listen):
        self.socket.listen(total_listen)
    
    def accept_connection(self):
        self.connection, self.client_address = self.socket.accept()
    
    def receive_message(self):
        message = self.connection.recv(self.buffer)
        return message.decode("utf-8")
    
    def send_message(self, message):
        self.connection.send(message)

    def close_connection(self):
        self.socket.close()
        print("Connection closed.")
    








