import sys
import os
import time
sys.path.insert(0, os.path.abspath('../../'))
from protocol.tcp_server import TCPServer

server = TCPServer()
print(server.__dict__)
if server.accept_connection():
    print("接続は完了しました")
    receive_m = server.receive_message()
    print("受取ったメッセージ", receive_m)
    server.send_request(receive_m)
    server.close_connection()

