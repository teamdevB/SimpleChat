import sys
import os
sys.path.insert(0, os.path.abspath('../../'))
from protocol.tcp_server import TCPServer


if __name__ == "__main__":
    server = TCPServer()
    server.start()

