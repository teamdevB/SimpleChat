from chat_room_list import ChatRoomList
from user import User
from protocol.tcp_server import TCPServer
from protocol.udp_server import UDPServer
import threading
class ServerModel:
    def __init__(self):
        self.tcp_host_server = TCPServer()
        self.udp_host_server = UDPServer()
        self.chat_room_list = ChatRoomList()
        self.clients = {}
        self.tokens = {}
    def start_server(self):
        tcp_server = self.tcp_host_server.socket 
        tcp_servers =tcp_server.bind(self.tcp_host_server.address,self.tcp_host_server.port)
        udp_server = self.udp_host_server.socket
        udp_servers = udp_server.bind(self.udp_host_server.server_address)
        threading.Thread(target=self.tcp_handler, args=(tcp_servers,)).start()
        threading.Thread(target=self.udp_handler, args=(udp_servers,)).start()
        
    def tcp_handler(self, server):
        pass  # TCPの処理を記述する

    def udp_handler(self, server):
        pass  # UDPの処理を記述する