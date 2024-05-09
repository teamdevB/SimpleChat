import socket
import json

class BaseSocket:
    def __init__(self):
        self.server_address = 'localhost'
        self.server_port = 9001
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 4096
        self.init_data()

    def init_data(self):
        # ヘッダー情報をbytesで初期化
        self.room_name_size = (0).to_bytes(1, 'big')
        self.operation = (0).to_bytes(1, 'big')
        self.state = (0).to_bytes(1, 'big')
        # ボディ情報をbytesで初期化
        self.room_name = b'\x00' * 8
        self.user_name = b'\x00' * 5
        self.password = b'\x00' * 8
        self.token = b'\x00' * 8

    def send_request(self, received_dict):
        try:
            self.dict_to_bytes(received_dict)
            self.set_head_and_body()
            self.socket.sendall(self.header + self.body)
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.close_connection()  # エラー発生時に接続を閉じる
            return False
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

    
    def close_connection(self):
        if self.socket:
            try:
                self.socket.close()
                print("Connection closed.")
            except socket.error as e:
                print(f"Error closing socket: {e}")
            finally:
                self.socket = None

    def set_head_and_body(self):
        self.header = self.room_name_size + self.operation + self.state
        self.body = self.room_name + self.user_name + self.password + self.token


    def header_and_body_to_dict(self, response_bytes):
        # 各フィールドの固定バイト位置を前提として解析
        self.room_name_size = response_bytes[0]
        self.operation = response_bytes[1]
        self.state = response_bytes[2]
        self.room_name = response_bytes[3:11]
        self.user_name = response_bytes[11:16]
        self.password = response_bytes[16:24]
        self.token = response_bytes[24:32]

        # ディクショナリに変換
        response_dict = {
            'room_name': self.room_name.decode('utf-8').rstrip('\x00'),
            'operation': int.from_bytes(self.operation, 'big'),
            'state': int.from_bytes(self.state, 'big'),
            'username': self.user_name.decode('utf-8').rstrip('\x00'),
            'password': self.password.decode('utf-8').rstrip('\x00'),
            'token': self.token.decode('utf-8').rstrip('\x00')
        }
        return response_dict


    def dict_to_bytes(self, dict):
        self.room_name = dict['room_name'].encode('utf-8').ljust(8, b'\x00')
        self.operation = dict['operation'].to_bytes(1, 'big')
        self.state = dict['state'].to_bytes(1, 'big')
        self.user_name = dict['username'].encode('utf-8').ljust(5, b'\x00')
        self.password = dict['password'].encode('utf-8').ljust(8, b'\x00')
        self.token = dict['token'].encode('utf-8').ljust(8, b'\x00')




class BaseUDP:
    def __init__(self, server_address='localhost', server_port=9001):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer = 4096

    def send_data(self, address, data_dict):
        data_bytes = json.dumps(data_dict).encode('utf-8')
        self.socket.sendto(data_bytes, address)

    def receive_data(self):
        data_bytes, address = self.socket.recvfrom(self.buffer)
        data_dict = json.loads(data_bytes.decode('utf-8'))
        return data_dict, address

    def close_socket(self):
        self.socket.close()
        print("Socket closed.")
