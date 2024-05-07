import socket
SERVER_HOST = 'localhost'
SERVER_PORT = 65432
class HostServer:
    def __init__(self):
        self.tcp_port = SERVER_PORT
        self.udp_port = SERVER_PORT

    def start_tcp_server(self):
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((SERVER_HOST, self.tcp_port))
        return tcp_server

    def start_udp_server(self):
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.bind((SERVER_HOST, self.udp_port))
        return udp_server

