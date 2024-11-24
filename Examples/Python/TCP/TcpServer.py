from socket import *

BUFFER_SIZE = 1000000

def main():
    # Create a TCP/IP socket
    serverSock = socket(AF_INET, SOCK_STREAM)

    # Initialize server address
    serverAddress = ('', 20000)

    # Bind the socket to the address
    try:
        serverSock.bind(serverAddress)
    except Exception as e:
        print("Bind failed:", e)
        serverSock.close()
        return

    # Start listening for incoming connections
    try:
        serverSock.listen(10)
    except Exception as e:
        print("Listen failed:", e)
        serverSock.close()
        return

    print("Server is ready and waiting for connections at port 20000")

    while True:
        try:
            # Wait for an incoming connection
            clientSock, clientAddress = serverSock.accept()
            print(f"Accepted a connection from {clientAddress[0]}:{clientAddress[1]}")

            while True:
                data = clientSock.recv(BUFFER_SIZE)
                if not data:
                    break

                print(f"Received {len(data)} bytes from the client")

            print("Client closed connection.")
            clientSock.close()

        except Exception as e:
            print("Error during connection handling:", e)
            break

    serverSock.close()

if __name__ == "__main__":
    main()
