from server.controller.server_controller import ServerController

def main():
    try:
        server = ServerController()
        server.start()
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
