from socket import *
from select import select

PORT1 = 20000
PORT2 = 30000
BUFFER_SIZE = 65507

def main():
    # Create UDP socket for port PORT1
    serverSock1 = socket(AF_INET, SOCK_DGRAM)
    serverSock1.bind(('', PORT1))

    # Create UDP socket for port PORT2
    serverSock2 = socket(AF_INET, SOCK_DGRAM)
    serverSock2.bind(('', PORT2))

    print("Server is ready and waiting for messages at UDP ports 20000 and 30000")

    while True:
        rset, _, _ = select([serverSock1, serverSock2], [], [])

        for sock in rset:
            data, peer = sock.recvfrom(BUFFER_SIZE)
            if sock is serverSock1:
                print(f"Received <{len(data)}> bytes from: {peer[0]}:{peer[1]}. My port: 20000")
            elif sock is serverSock2:
                print(f"Received <{len(data)}> bytes from: {peer[0]}:{peer[1]}. My port: 30000")

if __name__ == "__main__":
    main()
