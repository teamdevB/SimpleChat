from server_token import Token
import time
class User:
    def __init__(self, udp_addr=None, tcp_addr=None, join_token=None, user_name=None,is_host = False):
        self.udp_addr = udp_addr
        self.tcp_addr = tcp_addr
        self.join_token = Token().set_and_get_token() if join_token is None else join_token
        self.user_name = user_name
        self.last_sentmessage_time = time.time()
        self.self.is_host = is_host
    
    def get_user_name(self):
        return self.user_name

