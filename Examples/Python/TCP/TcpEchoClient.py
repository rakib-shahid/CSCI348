from socket import *

BUFFER_SIZE = 1000

def main():
    # Initialize client socket
    try:
        clientSock = socket(AF_INET, SOCK_STREAM)
    except socket.error as e:
        print(f"Unable to create the socket: {e}")
        return

    destIP = input("Enter TCP server's IP address: ")

    # Initialize server's IP + port and connect to the server
    serverAddress = (destIP, 20000)

    try:
        clientSock.connect(serverAddress)
        print("Connected to the server...")
    except socket.error as e:
        print(f"connect: {e}")
        clientSock.close()
        return

    msg_no = 1

    while True:
        msg = input(">>> ")
        if len(msg) == 0:
            continue

        if msg == "quit":
            break

        try:
            ret = clientSock.send(msg.encode('utf-8'))
            if ret < 0:
                print("send failed. Connection closed!")
                break

            buffer = clientSock.recv(BUFFER_SIZE)
            print(f"Received <{buffer.decode('utf-8')}> from the server")
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    clientSock.close()

if __name__ == "__main__":
    main()
