import socket
import json
import struct

class TCPClient():
    def __init__(self):
        self.server_address = 'localhost'
        self.server_port = 9001
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 4096

    def connect(self):
        self.socket.connect((self.server_address, self.server_port))
        print("Connected to the server at {}:{}".format(self.server_address, self.server_port))

    def send_request(self, room_name, user_name, password, operation, state):
        room_name_bytes = room_name.encode('utf-8')
        room_name_size = len(room_name_bytes)
        user_name_bytes = user_name.encode('utf-8')
        password_bytes = password.encode('utf-8')
        
        # ヘッダーの準備
        header = struct.pack('!BBB', room_name_size, operation, state)
        # ペイロードの準備
        # データを固定長でエンコード（余った部分は空白や特定の文字で埋める）
        room_name_padded = room_name_bytes.ljust(20, b'\x00')  # 20バイトになるようにパディング
        user_name_padded = user_name_bytes.ljust(15, b'\x00')  # 15バイトになるようにパディング
        password_padded = password_bytes.ljust(12, b'\x00')   # 12バイトになるようにパディング

        # ペイロードの作成
        payload = room_name_padded + user_name_padded + password_padded

        payload_size = len(payload)
        
        # メッセージの全体を送信
        self.socket.sendall(header + payload)
        print("Request sent to server.")

    def send_message(self, message_dict):
        # JSON形式でメッセージをエンコードして送信
        message_json = json.dumps(message_dict).encode('utf-8')
        self.socket.sendall(message_json)
        print("Message sent to server.")
    
    def receive_message(self):
        # サーバからの応答をJSON形式で受信してデコード
        response = self.socket.recv(self.buffer)
        return json.loads(response.decode('utf-8'))
    
    def close_connection(self):
        self.socket.close()
        print("Connection closed.")









    
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


# 使用例
if __name__ == "__main__":
    client = TCPClient()
    client.connect()
    client.send_request("Room1", "user123", "pass123", 1, 0)
    response = client.receive_response()
    print("Received from server:", response)
    client.close_connection()


# dictで受け取ったら、bytesに変換して送信
# bytesを変換してdiceで送信