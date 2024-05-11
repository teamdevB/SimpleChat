import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('../../'))
from protocol.tcp_client import TCPClient

dic = {
    'room_name': "roomname",
    'operation': 7,
    'state': 1,
    'username': "user",
    'password': "password",
    'token': "token"
}

client = TCPClient()
client.send_request(dic)
receive_dic = client.receive_message()
print("serverから受け取ったメッセージ: ", receive_dic)
client.close_connection()