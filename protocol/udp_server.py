import socket

class UDPServer:
    def __init__(self, host='0.0.0.0', port=9001):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.server_address)
        print(f"Server is running on {host}:{port}")
    
    def listen(self, room_members):
        print("Waiting for messages...")
        while True:
            message, client_address = self.socket.recvfrom(4048)
            print(f"Received message from {client_address}: {message.decode('utf-8')}")
            for member in room_members:
                if client_address != member.client_address:  # 送信元には送らない
                    self.socket.sendto(message, client_address)
    
    def close(self):
        self.socket.close()
        print("Server shut down.")
