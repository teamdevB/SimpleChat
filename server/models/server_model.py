from chat_room_list import ChatRoomList
from host_server import HostServer
import threading
class ServerModel:
    def __init__(self):
        super().__init__()
        ChatRoomList.__init__(self)
        self.clients = {}
        self.tokens = {}
    def start_server(self):
        tcp_server = self.start_tcp_server()
        udp_server = self.start_udp_server()
        threading.Thread(target=self.tcp_handler, args=(tcp_server,)).start()
        threading.Thread(target=self.udp_handler, args=(udp_server,)).start()
        
    def tcp_handler(self, server):
        pass  # TCPの処理を記述する

    def udp_handler(self, server):
        pass  # UDPの処理を記述する