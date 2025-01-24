"""
server.py Chat application server implementation using Python's socket programming capabilities

server.py provides the server-side implementation for a simple chat application 
using Python's socket programming capabilities. The server manages user authentication,
chatroom creation, message broadcasting, and client communication. It uses SQLite
for user and chatroom data storage and bcrypt for secure password hashing. The server
accepts incoming client connections and manages client communication through separate 
threads. It also features a server management menu for graceful shutdown and server administration. 

@author Osagie Owie
@email owieo204@potsdam.edu
@course CIS 480 Senior Project
@assignment Senior Project
@due 3/1/2025
"""

import socket # Enables TCP/IP networking for client-server communication between chat users
from threading import Thread # Handles concurrent client connections and message processing
import sqlite3 # Manages user accounts and chat history in SQL database
import bcrypt # Provides secure password hashing for user authentication
import os # Handles operating system operations like clearing terminal and process management
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich import print
from rich.layout import Layout
from rich.spinner import Spinner
from time import sleep
from rich.live import Live
from rich.tree import Tree
from datetime import datetime
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import select 
from rich.live import Live
from rich.table import Table
from datetime import datetime
from threading import Event
import time


class Server:

    clients = [] # Maintains a list of active client socket connections for managing client communication 
    chatrooms = {} # Dictionarty to map chatroom names to their metadata 
    active_chatrooms = {}  # New dictionary to track active members in chatrooms


    """
    __init__ Initializer to initialize the server and up core components

    __init__ establishes the server's socket configuration, database initialization, and server menu creation.
    It creates a TCP socket by binding to the specified host and port, and begins listening for incoming 
    connections. The method also initializes the database, sets up client tracking, and 
    launches the server management menu in a separate thread.

    @param HOST: String representing the server's IP address or hostname
    @param PORT: Integer representing the port number to listen on
    """
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address
        self.socket.bind((HOST, PORT))
        self.socket.listen(10) # Listen for up to 10 connections
        self.initialize_database()
        self.client_info = {}  # Store client info
        self.running = True # Server running status flag

        # Start the menu thread
        Thread(target=self.server_menu, daemon=True).start()

    """
    initialize_database Sets up the SQLite database schema for the chat application

    initialize_database creates and initializes the SQLite database with necessary tables
    for the chat application functionality. It sets up the database schema including
    tables for users, chatrooms, chatroom memberships, and messages.

    Database Schema Details:
        users table:
        - user_id: Unique identifier for each user
        - username: Unique user name
        - password_hash: Hashed password value
        - salt: Salt value for password hashing

        chatrooms table:
        - chatroom_id: Unique identifier for each chatroom
        - name: Unique chatroom name
        - admin_id: Foreign key linking to users table for room administrator

        chatroom_members table:
        - Composite primary key of chatroom_id and user_id
        - Tracks membership of users in chatrooms
        - Foreign keys to both chatrooms and users tables

        messages table:
        - message_id: Unique identifier for each message
        - Foreign keys to link messages to chatrooms and users
        - Includes message content and timestamp
        - Tracks message history with sender and chatroom context

    @param self: The server instance 
    """
    def initialize_database(self):
        conn = sqlite3.connect('chat_app.db')  # Connect to the database
        cursor = conn.cursor() 

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL            
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
            PRIMARY KEY (chatroom_id, user_id),
            FOREIGN KEY (chatroom_id) REFERENCES chatrooms (chatroom_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )''')

        # Creating messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chatroom_id INTEGER,
            user_id INTEGER,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chatroom_id) REFERENCES chatrooms (chatroom_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS private_messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            recipient_id INTEGER,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            read INTEGER DEFAULT 0,
            FOREIGN KEY (sender_id) REFERENCES users (user_id),
            FOREIGN KEY (recipient_id) REFERENCES users (user_id)
        )''')


        conn.commit()
        conn.close()

    """
    listen Accepts and manages incoming client connections 

    listen While the server is active, listen is ran to accept any new client connections
    and create separate threads to handle each client. When a new connection is received, it
    stores the client socket in the server's client list and spawns a dedicated thread for
    handling that client's communications. The method runs continuously until the server is stopped.

    @param self The server instance
    """
    def listen(self):
       
        while self.running: # Continuously accepting new connections
            try:
                client_socket, address = self.socket.accept() # Wait for and accept new client connection
                print("Connection from:", address)

                Server.clients.append(client_socket) # Add new client socket to the list of connected clients

                Thread(target=self.handle_client, args=(client_socket,)).start() # Start new thread to handle this client's messages independently

            except Exception as e:
                if self.running:  # Only log errors if server is still running
                    print(f"Error accepting connection: {e}")
    #MARK: HandleClient                
    """
    handle_client Processes all incoming messages and commands from a connected client

    handle_client manages the entire communication lifecycle with a single client by continuously listening for messages 
    from client.py. It handles user authentication (registration/login), chatroom operations (creation, joining, messaging), and maintains
    client state. The method operates until the client disconnects or an error occurs. 
    Expected commands from the client include:
        - /register: New user registration
        - /login: User authentication
        - /create_chatroom: Create new chatroom
        - /join_chatroom: Join existing chatroom
        - /chatroom_message: Send message to chatroom
        - /view_chatroom_users: List users in chatroom
        - /chatroom_view: List all available chatrooms
        - /exit_chatroom: Leave current chatroom

    @param self The server instance
    @param client_socket Socket object representing the connected client's connection
    """
    def handle_client(self, client_socket):
        
        client_name = None 

        while True:
            try:
                message = client_socket.recv(1024).decode() # Receive and decode client message  

                if not message:
                    break

                if message.startswith("/register"): # Handle registration command
                    _, username, password = message.split(" ", 2) 
                    response = self.register_user(username, password)
                    client_socket.send(response.encode())
                    if "successful" in response: 
                        client_name = username
                        self.client_info[client_socket] = username  

                elif message.startswith("/login"): # Handle login command
                    _, username, password = message.split(" ", 2)
                    response = self.authenticate_user(username, password)
                    client_socket.send(response.encode())
                    if "successful" in response:
                        client_name = username 
                        self.client_info[client_socket] = username

                #elif message.startswith("/exit"): # Handle exit command
                    #os._exit(0)
                    #break
                    
                elif not client_name: # Block all other commands until client is authenticated
                    client_socket.send("Please login or register first.".encode())
                    continue

                elif message.startswith("/create_chatroom"): # Chatroom creation command
                    chatroom_name = message.split(" ", 1)[1]
                    response = self.create_chatroom(chatroom_name, client_name)
                    client_socket.send(response.encode())

                elif message.startswith("/join_chatroom"): # Chatroom joining command
                    chatroom_name = message.split(" ", 1)[1]
                    response = self.add_user_to_chatroom(chatroom_name, client_name)
                    print(response)
                    client_socket.send(response.encode())
                

                elif message.startswith("/chatroom_message"): # Chatroom message command
                    _, chatroom_name, chat_message = message.split(" ", 2)
                    self.broadcast_chatroom_message(chatroom_name, client_name, chat_message)

                elif message.startswith("/view_chatroom_users"): # Chatroom user list command
                    chatroom_name = message.split(" ", 1)[1]
                    response = self.view_chatroom_users(chatroom_name)
                    client_socket.send(response.encode())

                elif message.startswith("/chatroom_view"): # Chatroom list command
                    conn = sqlite3.connect('chat_app.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM chatrooms")
                    chatrooms = [row[0] for row in cursor.fetchall()]
                    conn.close()
                    client_socket.send(', '.join(chatrooms).encode())

                elif message.startswith("/exit_chatroom"):
                    chatroom_name = message.split(" ", 1)[1]
                    # Remove user from active chatroom members
                    if chatroom_name in self.active_chatrooms and client_name in self.active_chatrooms[chatroom_name]:
                        self.active_chatrooms[chatroom_name].remove(client_name)
                        # If chatroom is empty, remove it from active_chatrooms
                        if not self.active_chatrooms[chatroom_name]:
                            del self.active_chatrooms[chatroom_name]
                    client_socket.send("exit".encode())
                
                elif message.startswith("/send_private"):
                    try:
                        _, recipient, private_message = message.split(" ", 2)
                        response = self.send_private_message(client_name, recipient, private_message)
                        client_socket.send(response.encode())
                    except Exception as e:
                        error_msg = f"Error processing private message: {str(e)}"
                        print(error_msg)  # Server-side logging
                        client_socket.send(error_msg.encode())

                elif message.startswith("/get_messages"):
                    messages = self.get_private_messages(client_name)
                    client_socket.send(str(messages).encode())

                elif message.startswith("/mark_read"):
                    _, message_id = message.split(" ", 1)
                    self.mark_message_as_read(int(message_id))
                    client_socket.send("Message marked as read.".encode())
                
                elif message.startswith("/check_messages"):
                    self.check_unread_messages(client_socket)

            except Exception as e:
                print(f"Error handling client: {e}")
                # Remove user from all active chatrooms when they disconnect
                for chatroom in list(self.active_chatrooms.keys()):
                    if client_name in self.active_chatrooms[chatroom]:
                        self.active_chatrooms[chatroom].remove(client_name)
                        if not self.active_chatrooms[chatroom]:
                            del self.active_chatrooms[chatroom]
                
                if client_socket in Server.clients:
                    Server.clients.remove(client_socket)
                if client_socket in self.client_info:
                    del self.client_info[client_socket]
                client_socket.close()
                break
    
    """
    create_chatroom Creates a new chatroom in the database

    create_chatroom creates a new chatroom in the database with the name
    and admin. It executes an SQL insert query to create the chatroom, linking it to the admin user's ID. 

    @param chatroom_name String name for the new chatroom
    @param admin_name String username of the chatroom administrator
    @return String message indicating success or existing chatroom error
    """
    def create_chatroom(self, chatroom_name, admin_name):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO chatrooms (name, admin_id) VALUES (?, (SELECT user_id FROM users WHERE username = ?))",
                           (chatroom_name, admin_name)) # Insert new chatroom into the database
            conn.commit()
            return f"Chatroom '{chatroom_name}' created successfully."
        except sqlite3.IntegrityError:
            return f"Chatroom '{chatroom_name}' already exists."
        finally: # Always close the connection
            conn.close()

    """
    add_user_to_chatroom Adds a specified user to an existing chatroom

    add_user_to_chatroom manages the process of adding a user to a chatroom by updating the
    chatroom_members table. It first verifies the chatroom exists, then creates the 
    membership record linking the user to the chatroom.

    @param chatroom_name name of the target chatroom
    @param user_name username of the user to add
    @return message indicating success or non-existent chatroom error
    """
    def add_user_to_chatroom(self, chatroom_name, user_name):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT chatroom_id FROM chatrooms WHERE name = ?", (chatroom_name,))
        chatroom_id = cursor.fetchone() # Get the chatroom ID

        if not chatroom_id: # Check if chatroom exists
            return f"Chatroom '{chatroom_name}' does not exist."

        cursor.execute("INSERT OR IGNORE INTO chatroom_members (chatroom_id, user_id) VALUES (?, (SELECT user_id FROM users WHERE username = ?))",
                       (chatroom_id[0], user_name)) # Add user to chatroom
        conn.commit()
        conn.close()

        # Add user to active chatroom members
        if chatroom_name not in self.active_chatrooms:
            self.active_chatrooms[chatroom_name] = set()
        self.active_chatrooms[chatroom_name].add(user_name)

        return f"Joined chatroom '{chatroom_name}'."

    """
    view_chatroom_users Retrieves a list of all users in the specified chatroom

    view_chatroom_users queries the database to get all usernames of members in a given
    chatroom. 
    
    @param chatroom_name String name of the chatroom to query
    @return String containing list of usernames 
    """
    def view_chatroom_users(self, chatroom_name):
        # Check if the chatroom exists in active_chatrooms
        if chatroom_name not in self.active_chatrooms:
            return f"No active users in chatroom '{chatroom_name}'."
        
        # Get the list of active users in the chatroom
        active_users = list(self.active_chatrooms[chatroom_name])
        
        if not active_users:
            return f"No active users in chatroom '{chatroom_name}'."
        
        return "Active users: " + ', '.join(active_users)

    """
    broadcast_chatroom_message Broadcasts a message to all members in a chatroom

    broadcast_chatroom_message handles the entire process of storing and distributing a chat
    message to all members of a chatroom. It saves the message to the database and broadcasts
    it to all connected clients who are members of the specified chatroom.

    Message Flow:
        Database Operations:
        - Verifies chatroom existence using chatroom name
        - Confirms sender exists in users table
        - Stores message in messages table with sender and chatroom info
        - Retrieves list of all chatroom members

        Message Broadcasting:
        - Formats message with sender and chatroom context
        - Iterates through all connected clients
        - Sends message to each client who is:
            1. Currently connected
            2. A member of the chatroom
            3. Not the original sender

    @param chatroom_name name of the target chatroom
    @param sender_name username of the message sender
    @param message content of the message to broadcast
    """
    def broadcast_chatroom_message(self, chatroom_name, sender_name, message):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT chatroom_id FROM chatrooms WHERE name = ?", (chatroom_name,))
            chatroom_id = cursor.fetchone() # Get the chatroom ID
            if not chatroom_id:
                return
            
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (sender_name,))
            user_id = cursor.fetchone() # Get the user ID
            if not user_id:
                return
            
            cursor.execute("INSERT INTO messages (chatroom_id, user_id, message) VALUES (?, ?, ?)",
                         (chatroom_id[0], user_id[0], message)) # Store the message in the database
            conn.commit()
            
            cursor.execute("""
                SELECT username 
                FROM users 
                JOIN chatroom_members ON users.user_id = chatroom_members.user_id 
                WHERE chatroom_id = ?
            """, (chatroom_id[0],)) # Get all members of the chatroom
            members = [row[0] for row in cursor.fetchall()] 
            
            formatted_message = f"[bold blue]{sender_name}[/bold blue]: {message}"
            
            for client_socket in Server.clients: # Broadcast message to all connected clients
                if client_socket in self.client_info:
                    username = self.client_info[client_socket]
                    if username in members and username != sender_name:
                        try:
                            client_socket.send(formatted_message.encode())
                        except:
                            Server.clients.remove(client_socket)
                            if client_socket in self.client_info:
                                del self.client_info[client_socket]
        finally:
            conn.close()

    """
    register_user Securely registers a new user in the database system
    
    register_user handles new user registration by validating password length,
    generating a unique salt, hashing the password with bcrypt, and storing the
    user credentials in the database. The method ensures password security through
    salting and hashing while maintaining username uniqueness.
      
    @param username: String containing desired username for registration
                    - Must be unique in the system
                    - Cannot be empty or None
    @param password: String containing user's chosen password
                    - Must be at least 8 characters long
                    - Will be hashed before storage
    @return: String message indicating registration statuses
    """
    def register_user(self, username, password):
        if len(password) < 8:
            return "Password must be at least 8 characters long."
            
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            
            salt = bcrypt.gensalt() # Generate a unique salt
            
            
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt) # Hash the password with the salt
            
            
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt) 
                VALUES (?, ?, ?)
            """, (username, password_hash.decode('utf-8'), salt.decode('utf-8'))) # Insert new user into the database
            
            conn.commit()
            return "Registration successful!" 
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e): # Check for unique username constraint violation
                return "Username already exists."
            return f"Registration failed: {str(e)}"
        finally:
            conn.close()

    """
    server_menu Displays and handles the server main menu
    
    server_menu provides a command-line interface for server administration, running
    in a continuous loop until the server is shut down. 
    The menu only currently provides the following options:
        1. Exit Server - Starts a graceful shutdown of the server
      
    @param self: Server instance  
    """
    #MARK: ServerMenu
    def server_menu(self):
        server_status = ServerStatus(self)
        
        with Live(
            server_status.generate_layout(),
            refresh_per_second=2,  # Update twice per second
            screen=True,  # Use alternate screen
            auto_refresh=True  # Enable automatic refresh
        ) as live:
            while self.running:
                try:
                    # Update the display
                    live.update(server_status.generate_layout())
                    
                    # Check for user input (non-blocking)
                    
                    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                    
                    if rlist:
                        choice = sys.stdin.readline().strip()
                        
                        if choice == '1':
                            # Pause live display
                            live.stop()
                            self.view_active_connections()
                            # Resume live display
                            live.start()
                        
                        elif choice == '2':
                            live.stop()
                            self.user_management_menu()
                            live.start()
                        
                        elif choice == '3':
                            #if self.confirm_shutdown():
                                self.shutdown_server()
                                break
                            
                        # Update immediately after handling command
                        live.update(server_status.generate_layout())
                    
                except Exception as e:
                    print(f"\nError in menu: {e}")
                    time.sleep(2)
                    continue
    
    """
    clear_terminal Clears the terminal screen across different operating systems

    clear_terminal The method uses os.name to detect the operating system and executes
    the appropriate terminal clear command through os.system(). 
    """
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear') # cls for Windows, clear for Unix

    """
    shutdown_server Performs a graceful shutdown of the chat server 

    shutdown_server orchestrates a clean server shutdown by executing these steps:
    1. Sets the running flag to False to stop main server loop
    2. Notifies all connected clients of shutdown
    3. Closes all client socket connections
    4. Closes the main server socket
    5. Terminates the server process

    @param self: Server instance
    """
    def shutdown_server(self):
        # Avoid duplicate shutdown calls
        if not self.running:
            return
        
        self.running = False
        
        # Broadcast a shutdown notice to all clients and close their sockets
        for client_socket in self.clients:
            try:
                client_socket.send("Server is shutting down...".encode())
            except:
                pass
            client_socket.close()
        
        self.clients.clear()
        
        # Close the server socket
        self.socket.close()
        print("[bold red]Server has shut down.[/bold red]")
        sys.exit(0)

    """
    authenticate_user Verifies user login credentials against stored database values
    
    authenticate_user Verifies user login credentials against stored database values by retrieving stored credentials, 
    extracting stored password hash and salt, hashing the provided password with the stored salt, and 
    comparing the hashed passwords for authentication.
    
    @param username: String containing the username to authenticate
    @param password: String containing the password to verify
    @return: String message of authentication result
    """
    def authenticate_user(self, username, password):
       
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            
            cursor.execute("""
                SELECT password_hash, salt 
                FROM users 
                WHERE username = ?
            """, (username,)) # Retrieve stored password hash and salt
            
            result = cursor.fetchone()
            if not result:
                return "Invalid username or password!"
                
            stored_hash, stored_salt = result # Extract stored hash and salt
            
            
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), 
                stored_salt.encode('utf-8') # Close server socket
            )
            
            
            if password_hash.decode('utf-8') == stored_hash: # Compare hashed passwords
                return "Login successful!"
            return "Invalid username or password."
            
        except Exception as e:
            return f"Authentication failed: {str(e)}"
        finally:
            conn.close()

    """
    view_active_connections - Displays list of currently connected clients
    
    view_active_connections creates a formatted table showing all active client 
    connections including username, IP address, port number and connection time
    for each connected client.
    
    @param self: Server instance
    """
    def view_active_connections(self):
        self.clear_terminal()
        console = Console()
        
        # Create a table for active connections
        from rich.table import Table
        table = Table(title="Active Connections", show_header=True, header_style="bold cyan")
        table.add_column("Username", style="cyan")
        table.add_column("IP Address", style="green")
        table.add_column("Port", style="yellow")
        table.add_column("Connected Since", style="magenta")
        
        
        console.print(table)
        input("\nPress Enter to return to main menu...")

    """
    view_server_logs - Displays recent server log entries
    
    view_server_logs reads and displays the last 20 entries from the server log
    file in a formatted panel. Shows error message if log file not found.
    
    @param self: Server instance
    """
    def view_server_logs(self):
        self.clear_terminal()
        console = Console()
        print(Panel.fit("[bold cyan]Recent Server Logs[/bold cyan]", border_style="cyan"))
        
        try:
            with open('server.log', 'r') as log_file:
                logs = log_file.readlines()[-20:]  # Show last 20 log entries
                for log in logs:
                    console.print(f"[grey70]{log.strip()}[/grey70]")
        except FileNotFoundError:
            print("[yellow]No log file found[/yellow]")
            
        input("\nPress Enter to return to main menu...")

    """
    get_private_messages - Retrieves private messages for a user
    
    get_private_messages queries the database for all private messages where the 
    specified user is the recipient, including sender info, message content,
    timestamp and read status.
    
    @param self: Server instance
    @param username: String username to get messages for
    @return: List of tuples containing message details
    """
    def get_private_messages(self, username):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    s.username as sender,
                    m.message,
                    m.timestamp,
                    m.message_id,
                    CASE WHEN m.read = 0 THEN 'Unread' ELSE 'Read' END as status
                FROM private_messages m
                JOIN users s ON m.sender_id = s.user_id
                JOIN users r ON m.recipient_id = r.user_id
                WHERE r.username = ?
                ORDER BY m.timestamp DESC
            """, (username,))
            return cursor.fetchall()
        finally:
            conn.close()

    """
    send_private_message - Sends a private message between users
    
    send_private_message stores private message in database and attempts immediate
    delivery if recipient is online. Handles both storage and delivery of private
    messages between users.
    
    @param self: Server instance
    @param sender_name: String username of message sender
    @param recipient_name: String username of message recipient 
    @param message: String content of the message
    @return: String status of message delivery
    """
    def send_private_message(self, sender_name, recipient_name, message):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            # Get sender and recipient IDs
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (sender_name,))
            sender_id = cursor.fetchone()
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (recipient_name,))
            recipient_id = cursor.fetchone()
            
            if not recipient_id:
                return "Recipient not found."
                
            # Store message in database
            cursor.execute("""
                INSERT INTO private_messages 
                (sender_id, recipient_id, message, timestamp, read) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, 0)
            """, (sender_id[0], recipient_id[0], message))
            conn.commit()
            
            # Check if recipient is online and send message
            recipient_socket = None
            for client_socket, username in self.client_info.items():
                if username == recipient_name:
                    recipient_socket = client_socket
                    break
                    
            if recipient_socket:
                formatted_message = f"[Private from {sender_name}]: {message}"
                try:
                    recipient_socket.send(formatted_message.encode())
                    return "Message sent and delivered successfully!"
                except:
                    return "Message stored but couldn't be delivered immediately."
            
            return "Message saved and will be delivered when recipient comes online."
            
        finally:
            conn.close()

    """
    mark_message_as_read - Marks a private message as read
    
    mark_message_as_read updates the read status to 1 in the database for the
    specified message ID.
    
    @param self: Server instance
    @param message_id: Integer ID of message to mark as read
    """
    def mark_message_as_read(self, message_id):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE private_messages SET read = 1 WHERE message_id = ?", (message_id,))
            conn.commit()
        finally:
            conn.close()

    """
    user_management_menu - Displays admin menu for user management
    
    user_management_menu provides interface for administrative tasks like viewing
    registered users and removing user accounts. Handles menu display and option
    selection.
    
    @param self: Server instance
    """
    def user_management_menu(self):
        while True:
            self.clear_terminal()
            console = Console()
            
            # Create menu table
            table = Table(show_header=False, header_style="cyan", border_style="cyan")
            table.add_row("[cyan]1[/cyan]", "[cyan]List All Users[/cyan]")
            table.add_row("[cyan]2[/cyan]", "[cyan]Remove User Account[/cyan]")
            table.add_row("[red]3[/red]", "[red]Return to Main Menu[/red]")
            
            console.print(Panel(table, title="[bold]User Management[/bold]", border_style="cyan"))
            
            choice = input(">> ")
            
            if choice == '1':
                self.list_registered_users()
            elif choice == '2':
                self.remove_user_account()
            elif choice == '3':
                break
            else:
                print(Panel("[red]Invalid choice[/red]", border_style="red"))
                time.sleep(1)

    """
    list_registered_users - Displays all registered users
    
    list_registered_users queries database for all registered usernames and
    displays them in a table with their current online/offline status.
    
    @param self: Server instance
    """
    def list_registered_users(self):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            # Get all registered users
            cursor.execute("SELECT username FROM users ORDER BY username")
            users = cursor.fetchall()
            
            console = Console()
            table = Table(title="Registered Users", show_header=True)
            table.add_column("Username", style="cyan")
            table.add_column("Status", style="green")
            
            # Check online status for each user
            for user in users:
                username = user[0]
                status = "[green]Online[/green]" if any(username == self.client_info[client] for client in self.client_info) else "[red]Offline[/red]"
                table.add_row(username, status)
            
            console.print(table)
            input("\nPress Enter to continue...")
            
        finally:
            conn.close()

    """
    remove_user_account - Removes a user account from the system
    
    remove_user_account removes specified user account and all associated data
    including messages, chatroom memberships etc. Handles database cleanup and
    disconnection if user is online.
    
    @param self: Server instance
    """
    def remove_user_account(self):
        
        username = input("\nEnter username to remove: ")
        
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if not user:
                print(Panel("[red]User not found[/red]", border_style="red"))
                time.sleep(1)
                return
            
            user_id = user[0]
            
            # Begin transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Remove user from chatrooms
            cursor.execute("DELETE FROM chatroom_members WHERE user_id = ?", (user_id,))
            
            # Remove user messages
            cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
            
            # Remove user private messages
            cursor.execute("DELETE FROM private_messages WHERE sender_id = ? OR recipient_id = ?", 
                        (user_id, user_id))
            
            # Remove the user
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            
            # 
            cursor.execute("COMMIT")
            
            print(Panel("[green]User account removed successfully[/green]", border_style="green"))
            time.sleep(1)
            
        except sqlite3.Error as e:
            cursor.execute("ROLLBACK")
            print(Panel(f"[red]Error removing user: {e}[/red]", border_style="red"))
            time.sleep(1)
        finally:
            conn.close()

    """
    get_unread_message_count - Retrieves count of unread messages for a user
    
    get_unread_message_count connects to the database and queries the private_messages
    table to count messages where read=0 for the specified recipient username.
    
    @param self: Server instance
    @param username: String username to check unread messages for
    @return: Integer count of unread messages
    """
    def get_unread_message_count(self, username):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM private_messages m
                JOIN users r ON m.recipient_id = r.user_id
                WHERE r.username = ? AND m.read = 0
            """, (username,))
            return cursor.fetchone()[0]
        finally:
            conn.close()

    """
    check_unread_messages - Checks and notifies client of unread messages
    
    check_unread_messages looks up unread message count for the client's username
    and if there are unread messages, sends a notification to the client's socket
    with the count.
    
    @param self: Server instance  
    @param client_socket: Socket object for the client to notify
    """
    def check_unread_messages(self, client_socket):
        if client_socket in self.client_info:
            username = self.client_info[client_socket]
            unread_count = self.get_unread_message_count(username)
            if unread_count > 0:
                notification = f"/notification You have {unread_count} unread message{'s' if unread_count > 1 else ''}!"
                try:
                    client_socket.send(notification.encode())
                except:
                    pass

    
"""
ServerStatus manages server monitoring interface display and real-time updates.

ServerStatus provides UI generation methods to display server metrics, active connections,
chatroom status and related information. Works with the server_menu() to create a live 
monitoring dashboard.
"""
class ServerStatus:
    def __init__(self, server):
        self.server = server
        self.stop_event = Event()


    """
    generate_layout Creates and updates the server monitoring interface layout

    @return: Layout object containing full server monitoring interface
    """
    def generate_layout(self) -> Layout:
    
        layout = Layout()
        
        # Create main layout structure
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )
        
        # Split header and body sections
        layout["header"].split_row(
            Layout(name="left"),
            Layout(name="middle"),
            Layout(name="right"),
        )
        
        layout["body"].split_row(
            Layout(name="menu", ratio=1),
            Layout(name="status", ratio=2),
        )
        
        # Update header with live information
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        layout["header"]["left"].update(
            Panel(
                Align.center(f"[cyan]Server Status: RUNNING[/cyan]\nTime: {current_time}"),
                style="green"
            )
        )
        layout["header"]["middle"].update(
            Panel(
                Align.center("[bold]Server Management Console[/bold]"),
                style="cyan"
            )
        )
        layout["header"]["right"].update(
            Panel(
                Align.center(
                    f"[green]Active Clients: {len(self.server.clients)}[/green]\n"
                ),
                style="green"
            )
        )
        
        # Menu options
        menu_content = """
1. [cyan]View Active Connections[/cyan]\n
2. [cyan]User Management[/cyan]\n
3. [red]Shutdown Server[/red]\n

        """
        layout["body"]["menu"].update(
            Panel(menu_content, title="[bold]Server Options[/bold]", border_style="cyan")
        )
        
        # Live status information
        status_content = self.generate_status_content()
        layout["body"]["status"].update(
            Panel(
                status_content,
                title="[bold]Server Status[/bold]",
                border_style="green"
            )
        )
        
        # Server details in footer
        addr = self.server.socket.getsockname()
        layout["footer"].update(
            Panel(
                Align.center(f"[dim]Listening on: {addr[0]}:{addr[1]}[/dim]"),
                style="cyan"
            )
        )
        
        return layout

    """
    generate_status_content creates status information for display

    @return: String containing formatted status details
    """
    def generate_status_content(self) -> str:
        
        status = []
        
        # Active clients section
        status.append("[bold cyan]Connected Clients:[/bold cyan]")
        for client_socket, username in self.server.client_info.items():
            try:
                addr = client_socket.getpeername()
                status.append(f"  • [green]{username}[/green] ({addr[0]}:{addr[1]})")
            except:
                continue
        
        # Active chatrooms section
        status.append("\n[bold cyan]Active Chatrooms:[/bold cyan]")
        for room_name, users in self.server.active_chatrooms.items():
            status.append(f"  • [yellow]{room_name}[/yellow] ({len(users)} users)")
            for user in users:
                status.append(f"    ◦ [green]{user}[/green]")
        
        return "\n".join(status)

    
if __name__ == '__main__':
    server = Server('127.0.0.1', 7632) # Uses Localhost IP for testing   
    server.listen() # Start listening for incoming connections