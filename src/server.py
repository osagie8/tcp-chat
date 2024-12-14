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
            
            # Get user ID and send it to the client
            user_id = self.get_user_id(client_name)
            client_socket.send(str(user_id).encode())

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

            if client_message.startswith("/create_chatroom"):
                chatroom_name = client_message.split(" ", 1)[1].strip()
                response = self.create_chatroom(chatroom_name, client_name)
                print("Response before sending:", response)
                client_socket.send(response.encode())
            # If the message is bye, remove the client from the list of clients and
            # close down the socket.
            elif client_message.strip() == client_name + ": bye" or not client_message.strip():
                self.broadcast_message(client_name, client_name + " has left the chat!")
                Server.Clients.remove(client)
                client_socket.close()
                break
            else: 
                # Send the message to all other clients
                self.broadcast_message(client_name, client_message)

    def create_chatroom(self, chatroom_name, admin_user_id):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO chatrooms (chatroom_name, admin_user_id) VALUES (?, ?)
            ''', (chatroom_name, admin_user_id))
            conn.commit()
            response = f"Chat room '{chatroom_name}' created successfully."
        except sqlite3.IntegrityError:
            response = f"Chat room '{chatroom_name}' already exists. Please choose a different name."
        except sqlite3.Error as e:
            response = f"An error occurred while creating the chat room: {e}"
        finally:
            conn.close()
        return response


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
        conn = sqlite3.connect('chat_app.db', timeout=30)
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
    
    def get_user_id(self, client_name):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (client_name,))
        user_id = cursor.fetchone()
        conn.close()
        return user_id[0] if user_id else None

    def create_chatroom(self, chatroom_name, admin_user_id):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO chatrooms (roomName, admin_id) VALUES (?, ?)
        ''', (chatroom_name, admin_user_id))
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
        chatroom_id INTEGER,
        user_id INTEGER,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chatroom_id) REFERENCES chatrooms (chatroom_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    # Create chatRooms table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chatrooms (
        chatroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roomName TEXT UNIQUE NOT NULL,
        admin_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,           
        FOREIGN KEY (admin_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close() 
   

if __name__ == '__main__':
    server = Server('127.0.0.1', 7632)
    server.listen()