import socket
from threading import Thread
import sqlite3

class Server:
    clients = []
    chatrooms = {}

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print('Server waiting for connections...')
        self.initialize_database()

    def initialize_database(self):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )''')

        # Create chatrooms table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatrooms (
            chatroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            admin_id INTEGER,
            FOREIGN KEY (admin_id) REFERENCES users (user_id)
        )''')

        # Create chatroom_members table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatroom_members (
            chatroom_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (chatroom_id) REFERENCES chatrooms (chatroom_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )''')

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
        )''')

        conn.commit()
        conn.close()

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print("Connection from:", address)
            client_name = client_socket.recv(1024).decode()

            self.add_user_to_db(client_name)
            client = {'socket': client_socket, 'name': client_name}
            Server.clients.append(client)

            print(f"{client_name} connected.")
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        client_socket = client['socket']
        client_name = client['name']

        while True:
            try:
                message = client_socket.recv(1024).decode()

                if message.startswith("/create_chatroom"):
                    chatroom_name = message.split(" ", 1)[1]
                    response = self.create_chatroom(chatroom_name, client_name)
                    client_socket.send(response.encode())

                elif message.startswith("/join_chatroom"):
                    chatroom_name = message.split(" ", 1)[1]
                    response = self.add_user_to_chatroom(chatroom_name, client_name)
                    client_socket.send(response.encode())

                elif message.startswith("/chatroom_message"):
                    _, chatroom_name, chat_message = message.split(" ", 2)
                    self.broadcast_chatroom_message(chatroom_name, client_name, chat_message)

                elif message.startswith("/exit_chatroom"):
                    chatroom_name = message.split(" ", 1)[1]
                    client_socket.send("exit".encode())

            except:
                self.clients.remove(client)
                client_socket.close()
                break

    def create_chatroom(self, chatroom_name, admin_name):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO chatrooms (name, admin_id) VALUES (?, (SELECT user_id FROM users WHERE username = ?))",
                           (chatroom_name, admin_name))
            conn.commit()
            return f"Chatroom '{chatroom_name}' created successfully."
        except sqlite3.IntegrityError:
            return f"Chatroom '{chatroom_name}' already exists."
        finally:
            conn.close()

    def add_user_to_chatroom(self, chatroom_name, user_name):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT chatroom_id FROM chatrooms WHERE name = ?", (chatroom_name,))
        chatroom_id = cursor.fetchone()

        if not chatroom_id:
            return f"Chatroom '{chatroom_name}' does not exist."

        cursor.execute("INSERT OR IGNORE INTO chatroom_members (chatroom_id, user_id) VALUES (?, (SELECT user_id FROM users WHERE username = ?))",
                       (chatroom_id[0], user_name))
        conn.commit()
        conn.close()
        return f"Joined chatroomed '{chatroom_name}'."

    def broadcast_chatroom_message(self, chatroom_name, sender_name, message):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()

        cursor.execute("SELECT chatroom_id FROM chatrooms WHERE name = ?", (chatroom_name,))
        chatroom_id = cursor.fetchone()
        if not chatroom_id:
            return

        cursor.execute("SELECT username FROM users JOIN chatroom_members ON users.user_id = chatroom_members.user_id WHERE chatroom_id = ?",
                       (chatroom_id[0],))
        members = [row[0] for row in cursor.fetchall()]
        conn.close()

        for client in Server.clients:
            if client['name'] in members and client['name'] != sender_name:
                client['socket'].send(f"{sender_name}@{chatroom_name}: {message}".encode())

    def add_user_to_db(self, client_name):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (client_name,))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    server = Server('127.0.0.1', 7632)
    server.listen()