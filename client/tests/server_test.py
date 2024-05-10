from protocol.tcp_server import TCPServer

server = TCPServer()

server.accept_connection()

send_dict = {
            'room_name': 'sample',
            'operation': 1,
            'state': 0,
            'username': 'username',
            'password': 'password',
            'token': 'token'
        }

#server.send_request(send_dict)
server.receive_message()
