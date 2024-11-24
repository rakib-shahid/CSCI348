from socket import *

def udp_server():
    # Create a UDP socket
    sock = socket(AF_INET, SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('', 20000)
    sock.bind(server_address)

    print('UDP server is up and listening on port 20000')

    BUFFER_SIZE = 65507
    while True:
        # Receive message
        data, address = sock.recvfrom(BUFFER_SIZE)
        
        # Print message size and sender's address
        print(f"Received {len(data)} bytes from {address}")

if __name__ == "__main__":
    udp_server()