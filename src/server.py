import socket
from threading import Thread
import sqlite3

class Server:
    Clients = []

    # Create a TCP socket over IPv4. Accept at max 5 connections.
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print('Server waiting for connection....')

        # Initialize the database
        initialize_database()

    # Listen for connections on the main thread. When a connection
    # is received, create a new thread to handle it and add the client
    # to the list of clients.
    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print("Connection from: " + str(address))
            
            # The first message will be the username
            client_name = client_socket.recv(1024).decode()

            # Add client to the database
            self.add_client_to_db(client_name)
            client = {'client_name': client_name, 'client_socket': client_socket}
            
            # Broadcast that the new client has connected
            self.broadcast_message(client_name, client_name + " has joined the chat!")
            
            Server.Clients.append(client)
            Thread(target=self.handle_new_client, args=(client,)).start()

    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']
        while True:
            # Listen out for messages and broadcast the message to all clients.
            client_message = client_socket.recv(1024).decode()
            # If the message is bye, remove the client from the list of clients and
            # close down the socket.
            if client_message.strip() == client_name + ": bye" or not client_message.strip():
                self.broadcast_message(client_name, client_name + " has left the chat!")
                Server.Clients.remove(client)
                client_socket.close()
                break
            else: 
                # Send the message to all other clients
                self.broadcast_message(client_name, client_message)

    # Loop through the clients and send the message down each socket.
    # Skip the socket if it's the same client.
    def broadcast_message(self, sender_name, message):
        # Add the message to the database
        self.add_message_to_db(sender_name, message)

        for client in self.Clients:
            client_socket = client['client_socket']
            client_name = client['client_name']
            if client_name != sender_name:
                client_socket.send(message.encode())
                
    def add_client_to_db(self, client_name):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO users (username) VALUES (?)
        ''', (client_name,))
        conn.commit()
        conn.close()

    def add_message_to_db(self, client_name, message):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO messages (user_id, message) VALUES (
            (SELECT user_id FROM users WHERE username = ?), ?
        )
        ''', (client_name, message))
        conn.commit()
        conn.close()            

def initialize_database():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    )
    ''')
    
    # Create messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close() 
   

if __name__ == '__main__':
    server = Server('127.0.0.1', 7632)
    server.listen()