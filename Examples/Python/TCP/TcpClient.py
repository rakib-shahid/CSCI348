from socket import *

BUFFER_SIZE = 100000

def main():
    # Create a TCP socket
    clientSock = socket(AF_INET, SOCK_STREAM)
    
    # Get the server IP address from the user
    destIP = input("Enter TCP server's IP address: ")
    
    # Initialize server address
    server_addr = (destIP, 20000)
    
    # Connect to the server
    try:
        clientSock.connect(server_addr)
        print("Connected to the server...")
    except Exception as e:
        print("connect:", e)
        clientSock.close()
        return

    while True:
        try:
            msg_size = int(input("Enter MsgSize [-1 to quit]>> "))
            if msg_size > BUFFER_SIZE:
                msg_size = BUFFER_SIZE
            if msg_size < 0:
                break
            
            buffer = b'A' * msg_size
            ret = clientSock.send(buffer)
            if ret < 0:
                print("send failed. Connection closed!")
        except Exception as e:
            print("Error:", e)
            break

    clientSock.close()

if __name__ == "__main__":
    main()
