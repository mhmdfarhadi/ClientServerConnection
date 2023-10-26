import socket
import threading

HEADER = 64
PORT = 5050
IP_SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (IP_SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            print(message)
        except:
            # Handle errors or disconnections here
            break

thread = threading.Thread(target=receive)
thread.start()

while True:
    client_msg = input("> ")
    if client_msg == DISCONNECT:
        send(DISCONNECT)
        print(f"{ADDR}: Disconnected!")
        break
    else:
        send(client_msg)

client.close()
