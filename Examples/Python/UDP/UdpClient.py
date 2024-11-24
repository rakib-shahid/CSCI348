from socket import *

BUFFER_SIZE = 65507

def main():
    # Create a UDP socket
    clientSock = socket(AF_INET, SOCK_DGRAM)

    buffer = bytearray(BUFFER_SIZE)
    while True:
        line = input("Enter <destIP> <destPort> <MsgSize> [-1 to quit] >> ")
        destIP, destPort, msgSize = line.split()
        destPort = int(destPort)
        msgSize = int(msgSize)

        if msgSize > BUFFER_SIZE:
            msgSize = BUFFER_SIZE
        if msgSize < 0:
            break

        # Initialize peer's address structure
        peer = (destIP, destPort)

        # Fill buffer with 'A'
        buffer = bytearray(b'A' * msgSize)

        # Send data to server
        ret = clientSock.sendto(buffer, peer)
        if ret < 0:
            print("Problem sending packet to the peer")
    
    clientSock.close()

if __name__ == "__main__":
    main()
