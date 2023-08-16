import socket
import threading
import tkinter as tk

HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

clients = {}
gamers = {}
client_sockets = []
offline_players = "3"

Allowed_IPs = [socket.gethostbyname(socket.gethostname())]

def add_IPs():
    allowed = Allowed_IP_entry.get()
    Allowed_IPs.append(allowed)
    print(Allowed_IPs)

def send_message_to_all_clients(message):
    for client in client_sockets:
        try:
            client.send(message.encode())
        except:
            client_sockets.remove(client)


def handle_client(connection, address):

    global offline_players
    if address in clients:
        print(f"[ALREADY CONNECTED] {address} tried to connect again.")
        connection.close()
        return

    if address not in gamers:
        gamers[address] = "Gamer " + str(len(gamers) + 1)
    
    if "Gamer 1" in gamers.values():
        gamer1_label.config(text="Gamer 1: Online")
    
    if "Gamer 2" in gamers.values():
        gamer2_label.config(text = "Gamer 2: Online")
    
    print(gamers)

    clients[address] = connection
    
    print(f"[NEW CONNECTION] {address} connected")
    
    client_sockets.append(connection)

    while True:
        try:
            data = connection.recv(1024).decode()
            if not data:
                break
        except:
            client_sockets.remove(connection)
            break

    connection.close()
    del clients[address]
    

    for key, value in gamers.items():
        if key == address:
            offline_players = value[len(value) - 1]

    if offline_players == "1":
        gamer1_label.config(text = "Gamer 1: Offline")

    elif offline_players == "2":
        gamer2_label.config(text = "Gamer 2: Offline")

    print(f"[DISCONNECTED] {address} disconnected")

    
def send_Start():
    send_message_to_all_clients("Game has started")

def send_Pause():
    send_message_to_all_clients("Game is paused")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        client_address = address[0]

        if client_address in Allowed_IPs:
            thread = threading.Thread(target = handle_client, args = (connection, address))
            thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients)}")
        

root = tk.Tk()
root.title("Server UI")

window_width = 400
window_height = 400
root.geometry(f"{window_width}x{window_height}")

#Add allowed IP addresses
Allowed_IP_label = tk.Label(root, text="Enter Gamer PC Allowed IPs")
Allowed_IP_label.pack()

Allowed_IP_entry = tk.Entry(root)
Allowed_IP_entry.pack()

Allowed_IP_button = tk.Button(root, text="Add", command=add_IPs)
Allowed_IP_button.pack()

gamer1_label = tk.Label(root, text="Games 1: Offline")
gamer1_label.pack()

gamer2_label = tk.Label(root, text="Gamer 2: Offline")
gamer2_label.pack()

start_button = tk.Button(root, text="Start Game", command=send_Start)
start_button.pack()

pause_button = tk.Button(root, text="Pause Game", command=send_Pause)
pause_button.pack()

listen_thread = threading.Thread(target=start)
listen_thread.start()

root.mainloop()