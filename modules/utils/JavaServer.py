import socket
import threading
import json
import numpy

MSG_LENGTH = 1024

PORT = 5000
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

class JavaServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg = conn.recv(MSG_LENGTH).decode(FORMAT)
            if msg:
                print("[DATA] RECEIVED: "+ str(msg))
        
                # x = {
                #         "Data": "received"
                #     }
                # y = json.dumps(x)
                y = "Hello client, this is the server"
                conn.send(y.encode(FORMAT))
                conn.send("\n".encode(FORMAT))
        conn.close()  

if __name__ == "__main__":
    server = JavaServer()
    server.start()