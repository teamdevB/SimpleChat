from client.controller.client_controller import ClientController

SERVER_HOST = 'localhost'
SERVER_PORT = 65432
BUFFER_SIZE = 4096


def main():
    try:
        client = ClientController()
        client.start()
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
