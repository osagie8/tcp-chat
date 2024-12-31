"""
client.py is the client-side implementation of the chat application. 

client.py connects to the server, authenticates the user, and provides a user interface for
interacting with the chat application. The client can create or join chatrooms, send messages,
view available chatrooms, access help, and exit the application. The client also listens for
incoming messages from the server and displays them to the user. 

@author Osagie Owie
@email owieo204@potsdam.edu
@course CIS 480 Senior Project
@assignment Senior Project
@due 3/1/2025
"""

import socket # Enables TCP/IP networking for client-server communication between chat users
from threading import Thread # Handles concurrent client connections and message processing
import os # Handles operating system operations like clearing terminal and process management
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich import print
from rich.layout import Layout

class Client:
    """
    Initilizies Client class by establishing a connection to the server setting up 
    the client's socket, and prompting the user for their name. The method then starts 
    a thread to handle incoming messages from the server and launches the main menu 
    for user interaction.

    @self: Client instance
    @param: HOST The IP address or hostname of the server to connect to
    @param: PORT The port number of the server 

    """
    def __init__(self, HOST, PORT):
        self.socket = socket.socket() 
        self.socket.connect((HOST, PORT)) 
        self.clear_terminal() 
        self.authenticate() 
        self.clear_terminal() 
        self.client_main_menu() # Display main menu for user interaction

    """
    authenticate Manages user authentication through login or registration menus.

    authenticate displays a menu for users to either log in with existing credentials or register
    as a new user. It handles the entire authentication flow including user input, server
    communication, and response processing. The method runs in a loop until successful
    authentication is achieved.

    @param self Client instance 
    """
    def authenticate(self):
        while True:
            print(Panel("Hello, Welcome to [green]Chitchat![/green] \n [green3] 1. Login [/green3] \n [dark_turquoise] 2. Register [/dark_turquoise]"))
            choice = input(">>")
            # Check the user's choice to either login or register
            if choice == '1':
                username = input("Username: ")
                password = input("Password: ")
                self.socket.send(f"/login {username} {password}".encode()) # Send login request to the server
            elif choice == '2':
                username = input("Choose username: ")
                password = input("Choose password: ")
                self.socket.send(f"/register {username} {password}".encode()) # Send register request to the server
            else:
                print("Invalid choice")
                continue
                
            response = self.socket.recv(1024).decode()
            if "success" in response.lower():
                self.name = username
                print("Authentication successful!")
                return
            else:
                print(response)
                print("Please try again")

    """
    client_main_menu method provides the main user interface for the chat application.

    client_main_menu method provides the main user interface for the chat application, 
    displaying options such as 'Create new chatroom' or 'Join existing chatroom', 'View available chatrooms', accessing 
    help, or exiting the application. The user input and sends corresponding commands 
    to the server, and processes the server’s responses to execute the selected action.

    """    
    def client_main_menu(self):
        while True:
            # Display main menu options
            print(Panel(Align.center("[green] Main Menu [/green]")))
            print(Panel(Align.center("[green] 1. Create new Chatroom [/green] \n [green] 2. Join existing Chatroom [/green] \n [green] 3. View available Chatrooms [/green] \n [green] 4. Help [/green] \n [green] 5. Exit [/green]")))

            #layout = Layout()
            #layout.split_column(Layout(Panel("Main Menu", style="green")),
            #Layout(name="lower")
            #)
            #layout["lower"].split_row(Layout(name="left"),
            #Layout(name="right"),
            #)
            #print(layout)
            #print("\nHello " + self.name + ", Welcome to the chat app!")


           
            choice = input("Enter your choice: ") # Get user input for menu choice

            if choice == '1': # Create new chatroom
                self.clear_terminal()
                chatroom_name = input("Enter chatroom name: ")
                self.socket.send(f"/create_chatroom {chatroom_name}".encode()) # Send chatroom creation request to the server
                response = self.socket.recv(1024).decode()  # Wait for server response after creating chatroom
                print(response)

            elif choice == '2': # Join existing chatroom
                self.clear_terminal()
                chatroom_name = input("Enter chatroom name to join: ")
                self.socket.send(f"/join_chatroom {chatroom_name}".encode()) # Send chatroom join request to the server
                response = self.socket.recv(1024).decode() # Wait for server response after joining chatroom
                print(response)
                if "Joined" in response:
                    self.chatroom_screen(chatroom_name)

            elif choice == '3': # View available chatrooms
                self.clear_terminal()
                print("Available chatrooms:")
                self.socket.send("/chatroom_view".encode()) # Send chatroom view request to the server
                response = self.socket.recv(1024).decode() # Wait for server response after viewing chatrooms
                print(response)

            elif choice == '4':
                self.help_screen() # Display help screen
                

            elif choice == '5': # Exit application
                self.socket.send("/exit".encode()) # Send exit request to the server
                print("Exiting...")
                self.socket.close()
                os._exit(0)

            else:
                self.clear_terminal()
                print("Invalid choice, try again.")

    """
    clear_terminal  Clears the terminal screen across different operating systems

    clear_terminal  The method uses os.name to detect the operating system and executes
    the appropriate terminal clear command through os.system(). 

    @param self: Server instance
    """            
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear') # cls for Windows, clear for Unix 

    """
    chatroom_screen Provides the chat interface for interacting within a chatroom

    chatroom_screen manages the chatroom user interface and message handling. It starts a message receiving thread, 
    and processes user input for sending messages and executing chatroom commands. The user can view chatroom users,
    send messages, and exit the chatroom. 

    @param self: Client instance 
    @param chatroom_name: String name of the chatroom to reference
    """
    def chatroom_screen(self, chatroom_name):
        self.clear_terminal()
        print(f"\033[1;32;40m{chatroom_name}\033[0m\n")
        print(f"Welcome to the chatroom {chatroom_name}! You (\033[4m {self.name} \033[0m) can start chatting now.")
        print("Type your messages below or type '/exit' to leave the chatroom.")
        print("Type '/view' to view users in chatroom.")
        Thread(target=self.receive_message, daemon=True).start() # Start thread to receive messages from the server
        
        while True:
            message = input("> ") # Chatroom message input
            if message.lower() == "/view": 
                self.socket.send(f"/view_chatroom_users {chatroom_name}".encode()) # Send request to view chatroom users
                response = self.socket.recv(1024).decode()
                print(response)

            if message.lower() == "/exit": # Exit chatroom
                self.socket.send(f"/exit_chatroom {chatroom_name}".encode()) # Send exit chatroom request to the server
                print("Exiting chatroom...")
                self.clear_terminal()
                break
            self.socket.send(f"/chatroom_message {chatroom_name} {message}".encode()) # Send message to chatroom
    
    """
    help_screen displays the help screen for the chat application.

    help_screen displays the help screen for the chat application, which contains information about
    the available commands and their usage. The help screen is read from a text file and displayed
    in the terminal.

    @param self: Client instance
    """
    def help_screen(self):
        self.clear_terminal() 
        file_path = "help.txt" 
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        if input("Press Enter to return to main menu.") == "":
            self.clear_terminal()
            self.client_main_menu()
    
    """
    receive_message continuously listens for messages from the server
     
    receive_message continuously listens for messages from the server and displays them to the user. 
    The method runs in a loop and breaks when the server sends an exit message.

    @param self: Client instance
    """
    def receive_message(self):
        while True:
            try:
                server_message = self.socket.recv(1024).decode() # Receive message from server
                if server_message == "exit":
                    print("You have been returned to the main menu.") # Return to main menu if chatroom is exited
                    break
                print(server_message)
            except:
                print("Connection closed by server.")
                self.socket.close()
                break

if __name__ == '__main__':
    client = Client('127.0.0.1', 7632) # Initialize client with server IP and port