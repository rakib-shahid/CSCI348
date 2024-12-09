# RAKIB SHAHID
# CSCI348 Project2

from socket import *
import sys
import threading
import time


# helper function to get content length
def get_length(host, path):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((host, 80))
        request = f"HEAD {path} HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())

        response = sock.recv(4096).decode()
        if "Content-Length" not in response:
            print("Failed to retrieve Content-Length.")
            sys.exit(1)

        sock.close()

        for line in response.split("\r\n"):
            if line.startswith("Content-Length"):
                return int(line.split(":")[1].strip())


# helper function for each thread to download their range of bytes
def download_range(host, path, start_byte, end_byte, output_file, thread_id):
    with socket(AF_INET, SOCK_STREAM) as clientSock:
        server_addr = (host, 80)
        try:
            clientSock.connect(server_addr)
        except Exception as e:
            print(
                f"Thread {thread_id}: Error connecting to server for range {start_byte}-{end_byte}: {e}"
            )
            clientSock.close()
            return

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Range: bytes={start_byte}-{end_byte}\r\n"
            f"Connection: close\r\n\r\n"
        )
        clientSock.send(request.encode())
        MSG_SIZE = 4096
        response = b""

        while True:
            chunk = clientSock.recv(MSG_SIZE)
            if not chunk:
                break
            response += chunk

        clientSock.close()

        if b"\r\n\r\n" in response:
            headers, body = response.split(b"\r\n\r\n", 1)

            # write the body to the file
            with open(output_file, "r+b") as f:
                f.seek(start_byte)
                f.write(body)
            print(
                f"Thread {thread_id} successfully downloaded range {start_byte}-{end_byte}."
            )
        else:
            print(
                f"Thread {thread_id} failed to download range {start_byte}-{end_byte}."
            )


# main function to parse arguments and start threads
def main():
    if len(sys.argv) != 4:
        print("Usage: python downloader.py NumberOfThreads ObjectURI localFilename")
        sys.exit(1)

    # parse arguments
    num_threads = sys.argv[1]
    host = sys.argv[2].split("/", 3)
    path = "/" + host[3]
    host = host[2]
    output_file = sys.argv[3]

    # validate number of threads
    if not num_threads.isdigit():
        print("NumberOfThreads must be an integer between 1 and 16.")
        sys.exit(1)
    num_threads = int(num_threads)
    if num_threads < 1 or num_threads > 16:
        print("NumberOfThreads must be an integer between 1 and 16.")
        sys.exit(1)

    print(f"Downloading from host: {host} (IP: {gethostbyname(host)}), path: {path}")

    # get content length and calculate chunk size
    content_length = get_length(host, path)
    print(f"FileSize: {content_length}")

    chunk_size = content_length // num_threads

    with open(output_file, "wb") as f:
        f.write(b"\0" * content_length)

    # start threads
    threads = []
    start_time = time.time()
    for i in range(num_threads):
        start_byte = i * chunk_size
        end_byte = (
            (start_byte + chunk_size - 1) if i != num_threads - 1 else content_length
        )
        thread = threading.Thread(
            target=download_range,
            args=(host, path, start_byte, end_byte, output_file, i),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end_time = time.time()

    print("Main thread terminating...")
    print(f"Total download time: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
