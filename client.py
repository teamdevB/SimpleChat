from client.controller.client_controller import ClientController

def main():
    try:
        client = ClientController()
        client.start()
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
