from socket import *

BUFFER_SIZE = 65507

def main():
    # Create a UDP socket
    clientSock = socket(AF_INET, SOCK_DGRAM)
    
    # Get the server IP address from the user
    destIP = input("Enter UDP server IP address: ")
    
    # Initialize server address
    peer = (destIP, 20000)
    
    while True:
        msg = input(">>> ")
        
        if msg == "quit":
            break
        
        # Send the message to the server
        try:
            clientSock.sendto(msg.encode(), peer)
        except Exception as e:
            print("Problem sending packet to the peer:", e)
            continue
        
        # Wait for the server to reply
        try:
            data, server = clientSock.recvfrom(BUFFER_SIZE)
            print(f"Server sent: <{data.decode()}>")
        except Exception as e:
            print("Error receiving from server. Server not running?", e)
    
    clientSock.close()

if __name__ == "__main__":
    main()
