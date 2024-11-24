# Rakib Shahid
from socket import *
from select import select
import os

BUFFER_SIZE = 65507
PORT = 20000
SERVER_ADDRESS = ("127.0.0.1", PORT)


def check_keyboard_input(buffer):
    if os.name == "nt":
        import msvcrt

        if msvcrt.kbhit():
            char = msvcrt.getwch()
            print(char, end="", flush=True)
            if char == "\r":
                print(flush=True)
                line = "".join(buffer)
                buffer.clear()
                return line
            elif char == "\b":
                if len(buffer) > 0:
                    buffer.pop()
                    line = "".join(buffer)
                    print("\b  ", end="", flush=True)
                    print(f"\r{line}", end="", flush=True)
            else:
                buffer.append(char)
                return None
    return False


def main():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    username = input("Enter your username: ").strip()
    client_socket.sendto(f"join:{username}".encode(), SERVER_ADDRESS)

    buffer = []
    while True:
        rset, _, _ = select([client_socket], [], [], 0.05)

        for sock in rset:
            data, _ = sock.recvfrom(BUFFER_SIZE)
            print(f"\n{data.decode()}")

        if line := check_keyboard_input(buffer):
            command = line
            if command == "leave":
                client_socket.sendto("leave".encode(), SERVER_ADDRESS)
                print("Left the chat.")
                break
            client_socket.sendto(command.encode(), SERVER_ADDRESS)

    client_socket.close()


if __name__ == "__main__":
    main()
