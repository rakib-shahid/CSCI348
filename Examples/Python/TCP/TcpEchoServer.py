from socket import *

BUFFER_SIZE = 1000

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

    while True:
        print("Server is ready and waiting for connections at port 20000")

        try:
            # Wait for an incoming connection
            clientSock, clientAddress = serverSock.accept()
            print(f"Accepted a connection from {clientAddress[0]}:{clientAddress[1]}")

            msg_no = 1

            while True:
                buffer = f"MsgNo[{msg_no:2d}]: "
                try:
                    data = clientSock.recv(BUFFER_SIZE - len(buffer))
                    if not data:
                        break
                    msg_no += 1
                    buffer += data.decode('utf-8')
                    print(f"Received <{buffer}> from the client")

                    # Echo back
                    clientSock.sendall(buffer.encode('utf-8'))
                except Exception as e:
                    print("Error receiving/sending data:", e)
                    break

            print("Client closed connection.")
            clientSock.close()

        except Exception as e:
            print("Error accepting connection:", e)
            break

    serverSock.close()

if __name__ == "__main__":
    main()
