import socket
import threading
import tkinter as tk
import requests
import datetime
import win32api


#Declaring variables
FORMAT = 'utf-8'
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

clients = {}
gamers = {}
client_sockets = []
offline_players = "3"

Allowed_IPs = [socket.gethostbyname(socket.gethostname())]
# print(Allowed_IPs)

def add_IPs():
    allowed = Allowed_IP_entry.get()
    Allowed_IPs.append(allowed)
    # print(Allowed_IPs)

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
    
    # print(gamers)

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

def uuid_generator():

    drive_letter = 'C:'

    drive_info = win32api.GetVolumeInformation(drive_letter + '\\')
    # print(drive_info[1])
    return drive_info[1]


def post_request():
    URL = 'https://vip.vr360action.com/machines/getServerTime'

    data = {"uuid": f'{uuid_generator()}'}

    response = requests.post(URL, json = data)

    server_time = response.json()
    server_time = server_time['serverTime'][0:10] +' ' + server_time['serverTime'][11:len(server_time['serverTime']) - 5]

    date_format = "%Y-%m-%d %H:%M:%S"
    date_time_obj = datetime.datetime.strptime(server_time, date_format)

    current_time = datetime.datetime.now()
    time_difference = date_time_obj - current_time
    return time_difference

def configuration_file():
    file_path = "hostIP.txt"
    file = open(file_path, "w")

    file.write(f"Host IP Address: {socket.gethostbyname(socket.gethostname())}")

    file.close()

configuration_file()

root = tk.Tk()
root.title("Server UI")

window_width = 400
window_height = 400
root.geometry(f"{window_width}x{window_height}")

server_label = tk.Label(root, text="Server up and running")
server_label.pack()

ip_label = tk.Label(root, text=f"Available at: {SERVER}")
ip_label.pack()

Allowed_IP_label = tk.Label(root, text="Add Gamer PC Allowed IPs")
Allowed_IP_label.pack(padx=10, pady=10)

Allowed_IP_entry = tk.Entry(root)
Allowed_IP_entry.pack(padx=10, pady=10)

Allowed_IP_button = tk.Button(root, text="Add", command=add_IPs)
Allowed_IP_button.pack(padx=10, pady=10)

gamer1_label = tk.Label(root, text="Gamer 1: Offline")
gamer1_label.pack(padx=10, pady=10)

gamer2_label = tk.Label(root, text="Gamer 2: Offline")
gamer2_label.pack(padx=10, pady=10)

start_button = tk.Button(root, text="Start Game", command=send_Start)
start_button.pack(padx=10, pady=10)

pause_button = tk.Button(root, text="Pause Game", command=send_Pause)
pause_button.pack(padx=10, pady=10)

time_label = tk.Label(root, text=f"Time Difference With The Server: {post_request()}")
time_label.pack(padx=10, pady=10)

listen_thread = threading.Thread(target=start)
listen_thread.start()

root.mainloop()