import tkinter as tk
import threading
import subprocess
import time
import socket

#This function creates a configuration file for the IP address
def configuration_file():
    file_path = "GamerIP.txt"
    file = open(file_path, "w")

    file.write(f"Host IP Address: {socket.gethostbyname(socket.gethostname())}")

    file.close()

#Initiasing the clients connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 5051
FORMAT = 'utf-8'

#Function to retun the server address
def server_address():
    SERVER = host_entry.get()
    return SERVER

#This function tries to connect to the server
def check_connection():
    host = host_entry.get()
    result_label.config(text="Currently Disconnecting. Trying..")

    SERVER = server_address()
    client.connect((SERVER, PORT))

    threading.Thread(target=ping_host, args=(host,)).start()
    threading.Thread(target=print_messages).start()

#This function writes messages as sent by the server
def print_messages():
    
    while True:
        game_label.config(text=client.recv(2048).decode(FORMAT))

#This function pings the host every few seconds to check the connection health
def ping_host(host):

    
    while True:
        try:
            response = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
            if response:
                result_label.config(text="Host is connected")
                
            else:
                result_label.config(text="Host is not connected")
        except subprocess.TimeoutExpired:
            result_label.config(text="Host is not reachable")

        time.sleep(5) #Sleep for 5 seconds

configuration_file()

#Main UI using tkinter
root = tk.Tk()
root.title("Client UI")

window_width = 400
window_height = 400
root.geometry(f"{window_width}x{window_height}")

host_label = tk.Label(root, text="Enter host IP")
host_label.pack(padx=10, pady=10)

host_entry = tk.Entry(root)
host_entry.pack(padx=10, pady=10)

check_button = tk.Button(root, text="Connect", command=check_connection)
check_button.pack(padx=10, pady=10)

game_label = tk.Label(root, text="")
game_label.pack(padx=10, pady=10)

result_label = tk.Label(root, text="")
result_label.pack(padx=10, pady=10)

listen_thread = threading.Thread(target=print_messages)
listen_thread.start()

# Start the main event loop
root.mainloop()

