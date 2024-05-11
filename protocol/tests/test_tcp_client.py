import sys
import os
sys.path.insert(0, os.path.abspath('../../'))
from protocol.tcp_client import TCPClient


client = TCPClient()
while True:
    user_name = input("user_name -> ")
    room_name = input("room_name -> ")
    dic = {
        'room_name': room_name,
        'operation': 1,
        'state': 2,
        'user_name': user_name,
        'password': "password",
        'token': "token"
    }
    client.send_request(dic)
    receive_dic = client.receive_message()
    print("serverから受け取ったメッセージ: ", receive_dic)
