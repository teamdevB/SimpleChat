import socket

class UDPClient:
    def __init__(self, server_host='localhost', server_port=9001):
        self.server_address = (server_host, server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send_message(self, message):
        self.socket.sendto(message.encode('utf-8'), self.server_address)
        print(f"Sent message to server: {message}")
    
    def recieve_message(self):    
        response, _ = self.socket.recvfrom(4048) 
        response_message = response.decode('utf-8')
        print(f"Received response from server: {response_message}")
        return response_message
    
    def close(self):
        self.socket.close()
        print("Connection closed.")
