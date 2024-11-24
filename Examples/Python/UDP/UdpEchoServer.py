from socket import *

def main():
    # Create a UDP socket
    serverSock = socket(AF_INET, SOCK_DGRAM)

    # Initialize server address
    serverAddress = ('', 20000)
    
    # Bind the socket to the address
    try:
        serverSock.bind(serverAddress)
    except Exception as e:
        print("Bind error:", e)
        serverSock.close()
        return

    BUFFER_SIZE = 65507
    print("Server is ready and waiting for messages at UDP port 20000")
    msg_no = 1

    while True:
        try:
            # Receive message from client
            data, clientAddress = serverSock.recvfrom(BUFFER_SIZE)
            if not data:
                break

            msg = f"MsgNo[{msg_no:2d}]: {data.decode()}"
            msg_no += 1

            print(f"Received <{data.decode()}> from: {clientAddress[0]}:{clientAddress[1]}")

            # Echo the message back to the client
            serverSock.sendto(msg.encode(), clientAddress)
        
        except Exception as e:
            print("Error receiving from client:", e)
            break

    serverSock.close()

if __name__ == "__main__":
    main()
