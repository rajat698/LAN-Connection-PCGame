import tkinter as tk
import threading
import subprocess
import time
import socket

HEADER = 64
FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5050

def server_address():
    SERVER = host_entry.get()
    return SERVER


def check_connection():
    host = host_entry.get()
    result_label.config(text="Checking")

    SERVER = server_address()
    client.connect((SERVER, PORT))
    
    threading.Thread(target=ping_host, args=(host,)).start()
    threading.Thread(target=print_messages).start()

def print_messages():
    
    while True:
        game_label.config(text=client.recv(2048).decode(FORMAT))

def ping_host(host):

    
    while True:
        try:
            response = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
            if response:
                result_label.config(text="Host is connected")
                # print(response)
            else:
                result_label.config(text="Host is not connected")
        except subprocess.TimeoutExpired:
            result_label.config(text="Host is not reachable")

        time.sleep(5) #Sleep for 5 seconds

# Create the main window
root = tk.Tk()
root.title("Client UI")

window_width = 400
window_height = 400
root.geometry(f"{window_width}x{window_height}")

# Create and pack widgets
host_label = tk.Label(root, text="Enter host IP")
host_label.pack()

host_entry = tk.Entry(root)
host_entry.pack()

check_button = tk.Button(root, text="Connect", command=check_connection)
check_button.pack()

game_label = tk.Label(root, text="")
game_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

listen_thread = threading.Thread(target=print_messages)
listen_thread.start()

# Start the main event loop
root.mainloop()
