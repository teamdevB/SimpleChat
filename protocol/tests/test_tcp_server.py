import sys
import os
import time
sys.path.insert(0, os.path.abspath('../../'))
from protocol.tcp_server import TCPServer

server = TCPServer()
if server.accept_connection():
    print("接続は完了しました")
    receive_m = server.receive_message()
    print("clientから受取ったメッセージ:", receive_m)
    receive_m["room_name"] = "ctake"
    receive_m["operation"] = 12
    server.send_request(receive_m)
    server.close_connection()

