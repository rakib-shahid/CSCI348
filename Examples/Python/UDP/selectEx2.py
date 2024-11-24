# This code will in Unix-based systems (Linux/FreeBSD/MAC)
from socket import *
from select import select
import sys

PORT = 20000
BUFFER_SIZE = 65507

def main():
    # Create UDP socket for port PORT1
    serverSock = socket(AF_INET, SOCK_DGRAM)
    serverSock.bind(('', PORT))

    print("Server is ready and waiting for messages at UDP ports 20000 and the standard input")

    while True:
        rset, _, _ = select([serverSock, sys.stdin], [], [])

        for sock in rset:
            data, peer = sock.recvfrom(BUFFER_SIZE)
            if sock is serverSock:
                print(f"Received <{len(data)}> bytes from: {peer[0]}:{peer[1]}. My port: 20000")
            elif sock is sys.stdin:
                user_input = sys.stdin.readline().strip()
                print("User typed:", user_input)

if __name__ == "__main__":
    main()
