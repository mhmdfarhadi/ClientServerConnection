import socket
import threading

HEADER = 64
PORT =  5050
IP_SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (IP_SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# A list to keep track of connected clients
clients_list = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} is connected")

    conncted = True
    while conncted:
        try :
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                
                if msg == DISCONNECT:
                    print(f"[{addr}] disconnected")
                    conncted = False
                    
                print(f"[{addr}] : {msg}")

                # Broadcast the message to all connected clients
                broadcast(msg, conn, addr)
        except ConnectionResetError:# if one client close terminal it will crash so this will prevent it
            print(f"[{addr}] disconnected")
            conncted = False

    conn.close()

def broadcast(message, sender_conn, addr):
    for client in clients_list:
        if client != sender_conn:
            #try:
                client.send(message.encode(FORMAT))
            #except:
                # If there's an error sending to a client, remove that client
                #remove(client)

def remove(client):
    if client in clients_list:
        clients_list.remove(client)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {IP_SERVER}")
    while True:
        conn, addr = server.accept()
        clients_list.append(conn)  # Add the new client connection to the list
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active Connections: {threading.active_count() - 1}")

print("Server has started...")
start()
