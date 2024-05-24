import time
class User:
    def __init__(self, udp_addr=None, tcp_addr=None,  user_name=None):
        self.tcp_addr = tcp_addr
        self.user_name = user_name
        self.last_sentmessage_time = time.time()

    
    def get_user_name(self):
        return self.user_name
