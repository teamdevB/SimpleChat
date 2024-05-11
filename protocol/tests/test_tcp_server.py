import sys
import os
import time
sys.path.insert(0, os.path.abspath('../../'))
from protocol.tcp_server import TCPServer

server = TCPServer()
server.start_server()

