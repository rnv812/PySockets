import socket

from handler import Handler


HOST = "127.0.0.1"  # run on local machine
PORT = 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))

    print(f"Listening on {HOST}:{PORT}")
    sock.listen(10)

    while True:
        conn, addr = sock.accept()

        with conn:
            print(f"Got a connection from {addr}")

            data = conn.recv(1024)
            result = Handler(data).execute()
            conn.sendall(result)

            conn.close()
