from super_protocol import BaseUDP
import json

class UDPServer(BaseUDP):
    def __init__(self):
        super().__init__()
        self.socket.bind((self.server_address, self.server_port))
        self.clients = set()
        print(f"UDP Server listening on {self.server_address}:{self.server_port}")

    def run(self):
        print("Server is running and waiting for messages...")
        try:
            while True:
                data_bytes, address = self.socket.recvfrom(4096)
                data_dict = json.loads(data_bytes.decode('utf-8'))
                self.clients.add(address)  # 受信したクライアントのアドレスを記録
                print(f"Received message from {address}: {data_dict}")
                self.broadcast(data_dict, address)
        except KeyboardInterrupt:
            print("Server is shutting down.")
        finally:
            self.socket.close()

    def broadcast(self, message, sender_address):
        """受け取ったメッセージを登録されたクライアント全員に送信する（送信者を除く）。"""
        for client_address in self.clients:
            if client_address != sender_address:  # 送信者自身には送らない
                data_bytes = json.dumps(message).encode('utf-8')
                self.socket.sendto(data_bytes, client_address)