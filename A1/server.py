# Rakib Shahid
from socket import *
from select import select

BUFFER_SIZE = 65507
PORT = 20000
clients = {}


def handle_client_message(message, client_address, server_socket):
    message = message.strip()
    if message.startswith("join:"):
        username = message.split(":", 1)[1]
        clients[username] = client_address
        print(f"{username} joined. Total users: {len(clients)}")
    elif message == "users":
        user_list = ", ".join(clients.keys())
        server_socket.sendto((f"Online Users: {user_list}").encode(), client_address)
    elif message.startswith("to"):
        out_message = message[message.find("msg") + 4 :]
        parts = message.split()
        from_user = [key for key, value in clients.items() if value == client_address][
            0
        ]
        if len(parts) <= 1 or "msg" not in message:
            server_socket.sendto("Invalid command.".encode(), client_address)
        else:
            if parts[1] == "all":
                msg = out_message
                for addr in clients.values():
                    if addr != client_address:
                        server_socket.sendto(f"{from_user}: <{msg}>".encode(), addr)
            else:
                recipients = message[: message.find("msg") - 1].split()[1:]
                msg = out_message
                for recipient in recipients:
                    if recipient in clients:
                        server_socket.sendto(
                            f"{from_user}: <{msg}>".encode(), clients[recipient]
                        )
                    else:
                        server_socket.sendto(
                            f"Error: {recipient} not online.".encode(), client_address
                        )

    elif message == "leave":
        username = next(
            (user for user, addr in clients.items() if addr == client_address), None
        )
        if username:
            del clients[username]
            print(f"{username} left. Total users: {len(clients)}")
    else:
        server_socket.sendto("Invalid command.".encode(), client_address)


def start_server():
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(("", PORT))
    print(f"Server is running on port {PORT}")

    while True:
        rset, _, _ = select([server_socket], [], [])
        for sock in rset:
            data, client_address = sock.recvfrom(BUFFER_SIZE)
            handle_client_message(data.decode(), client_address, server_socket)


if __name__ == "__main__":
    start_server()
