import socket
import threading
import select

IP = "0.0.0.0"
PORT = 6789
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    # TCP connection set up
    conn.setblocking(0)
    connected = True
    while connected:
        ready = select.select([conn], [], [], 10)
        if ready[0]:
            msg = conn.recv(SIZE).decode(FORMAT)
            print(f"[ORIGINAL MESSAGE] {msg}")
            filename = msg.split()[1]
            f = open(filename[1:])
            print(f"[{addr}] {msg}")

            outputdata = f.read()
            # Send the connection message
            conn.send(bytes("HTTP/1.1 200 OK","UTF-8"))
            conn.send(outputdata.encode())
        else:
            break

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()