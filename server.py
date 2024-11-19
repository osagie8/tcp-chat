'''
server.py is the Server for the TCP chat application.

  @author Osagie Owie
  @email owieo204@potsdam.edu
  @course CIS 480 Senior Project
  @assignment: Senior Project
  @due 12/9/24 
 '''

import socket
import threading

# Server settings
HOST = "127.0.0.1"  # Localhost
PORT = 9090         # Port number

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()  # Listen for incoming connections

clients = []

# Function to broadcast messages to all clients except the sender
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

# Function to handle communication with a single client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break

# Start the server
print(f"Server started on {HOST}:{PORT}")

while True:
    client, address = sock.accept()
    print(f"{address} connected")
    client.send("Welcome to the chat room!".encode())
    clients.append(client)
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()
