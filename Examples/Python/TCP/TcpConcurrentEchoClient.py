from socket import *
from threading import Thread

BUFFER_SIZE = 1000

def talkToClient(clientSock):
    msg_no = 1

    while True:
        buffer = f"MsgNo[{msg_no:2d}]: ".encode('utf-8')
        msg_no += 1

        try:
            data = clientSock.recv(BUFFER_SIZE - len(buffer))
            if not data:
                break

            buffer += data
            print(f"Received <{data.decode('utf-8')}> from the client")

            # Echo back
            clientSock.sendall(buffer)
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    print("Client closed connection.")
    clientSock.close()

def main():
    # Initialize server socket
    try:
        serverSock = socket(AF_INET, SOCK_STREAM)
    except socket.error as e:
        print(f"Unable to create the socket: {e}")
        return

    serverAddress = ('', 20000)  # Bind to all interfaces on port 20000

    try:
        serverSock.bind(serverAddress)
    except socket.error as e:
        print(f"Bind failed: {e}")
        serverSock.close()
        return

    try:
        serverSock.listen(10)
    except socket.error as e:
        print(f"Listen failed: {e}")
        serverSock.close()
        return

    print("Server is ready and waiting for connections at port 20000")

    while True:
        try:
            clientSock, client_addr = serverSock.accept()
        except socket.error as e:
            print(f"Accept failed: {e}")
            continue

        print(f"Accepted a connection..")
        print(f"clientIPAddr: {client_addr[0]}:{client_addr[1]}")

        # Create a thread to handle the request
        client_thread = Thread(target=talkToClient, args=(clientSock,))
        client_thread.start()

if __name__ == "__main__":
    main()
