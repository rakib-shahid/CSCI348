# This code will in Windows
from socket import *
from select import select
import sys
import os

PORT = 20000
BUFFER_SIZE = 65507

buffer = []
def checkKeyboardInput():
    if os.name == 'nt':  # Windows
        import msvcrt
        if msvcrt.kbhit():
            ch = msvcrt.getwch()  # Get a single character from the input
            print(ch, end='', flush=True)
            if ch == '\r':
                print(flush=True)
                line = "".join(buffer)
                buffer.clear()
                return line            
            elif ch == '\b':
                if len(buffer) > 0:
                    buffer.pop()
                    line = "".join(buffer)
                    print(f"\b  ", end='', flush=True)
                    print(f"\r{line}", end='', flush=True)
            else:
                buffer.append(ch)
                return None

def main():
    # Create UDP socket for port PORT1
    serverSock = socket(AF_INET, SOCK_DGRAM)
    serverSock.bind(('', PORT))

    print("Server is ready and waiting for messages at UDP port 20000")

    while True:
        # 0.05 second timeout
        rset, _, _ = select([serverSock], [], [], 0.05)  

        for sock in rset:
            data, peer = sock.recvfrom(BUFFER_SIZE)
            if sock is serverSock:
                print(f"Received <{len(data)}> bytes from: {peer[0]}:{peer[1]}. My port: 20000")

        line = checkKeyboardInput()
        if line is not None:
            print(f"User Typed: <{line}>")
            if line == "quit":
                sys.exit(0)

if __name__ == "__main__":
    main()
