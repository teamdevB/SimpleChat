from protocol.tcp_client import TCPClient


client = TCPClient()

client.connect()

# client.receive_message()

send_dict = {
            'room_name': 'sample',
            'operation': 1,
            'state': 0,
            'username': 'username',
            'password': 'password',
            'token': 'token'
        }

client.send_request(send_dict)

client.receive_message()
