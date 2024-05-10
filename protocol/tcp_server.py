from super_protocol import BaseSocket
import socket

class TCPServer(BaseSocket):
    def __init__(self):
        super().__init__()
        self.socket.bind((self.server_address, self.server_port))
        self.socket.listen(5)


    def accept_connection(self):
        try:
            self.connection, self.client_address = self.socket.accept()
            print(f"{self.client_address}からの接続を受け入れました")
            return True
        except socket.error as e:
            print(f"接続の受け入れ中にエラーが発生しました: {e}")
            return False
        
    def receive_message(self):
        try:
            response_bytes = self.connection.recv(self.buffer)
            if len(response_bytes) != 32:  # header+bodyは32bytes
                print("Received incomplete data.")
                return None
            return self.header_and_body_to_dict(response_bytes)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            self.close_connection()
            return None
    
if __name__ == "__main__":
    server = TCPServer()
    if server.accept_connection():
        print("確立しました")
        message = server.receive_message()
        print(message)