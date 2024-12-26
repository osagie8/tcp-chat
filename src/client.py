import socket
from threading import Thread
import os

class Client:
    """
    Constructor initializes the Client class by establishing a connection to the server, setting up 
    the client's socket, and prompting the user for their name. Once initialized, the method 
    starts a thread to handle incoming messages from the server and launches the main menu 
    for user interaction.

    @param:
    HOST (str): The IP address or hostname of the server to connect to.
    PORT (int): The port number of the server.

    """
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Enter your name: ")
        self.socket.send(self.name.encode())
        #Thread(target=self.receive_message).start()
        self.clear_terminal()
        self.client_main_menu()

    """
    client_main_menu method provides the main user interface for the chat application.

    client_main_menu method provides the main user interface for the chat application, 
    displaying options such as creating or joining chatrooms, viewing available chatrooms, accessing 
    help, or exiting the application. It handles user input, sends corresponding commands 
    to the server, and processes the server’s responses to execute the selected actions.

    """    

    def client_main_menu(self):
        while True:
            print("\033[1;32;40mMain Menu\n\033[0m")
            print("\nHello " + self.name + ", Welcome to the chat app!")
            print("1. Create new chatroom")
            print("2. Join existing chatroom")
            print("3. View available chatrooms")
            print("4. Help")
            print("5. Exit Application")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.clear_terminal()
                chatroom_name = input("Enter chatroom name: ")
                self.socket.send(f"/create_chatroom {chatroom_name}".encode())
                response = self.socket.recv(1024).decode()  # Wait for server response after creating chatroom
                print(response)

            elif choice == '2':
                self.clear_terminal()
                chatroom_name = input("Enter chatroom name to join: ")
                self.socket.send(f"/join_chatroom {chatroom_name}".encode())
                response = self.socket.recv(1024).decode()
                print(response)
                if "Joined" in response:
                    self.chatroom_screen(chatroom_name)

            elif choice == '3':
                self.clear_terminal()
                print("Available chatrooms:")
                self.socket.send("/chatroom_view".encode())
                response = self.socket.recv(1024).decode()
                print(response)

            elif choice == '4':
                self.help_screen()
                

            elif choice == '5':
                self.socket.send("/exit".encode())
                print("Exiting...")
                self.socket.close()
                os._exit(0)

            else:
                self.clear_terminal()
                print("Invalid choice, try again.")
                

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')            

    def chatroom_screen(self, chatroom_name):
        self.clear_terminal()
       #print("\033[2J\033[H", end="") # Clear terminal screen
        print(f"\033[1;32;40m{chatroom_name}\033[0m\n")
        print(f"Welcome to the chatroom {chatroom_name}! You (\033[4m {self.name} \033[0m) can start chatting now.")
        print("Type your messages below or type '/exit' to leave the chatroom.")
        print("Type '/view' to view users in chatroom.")
        Thread(target=self.receive_message, daemon=True).start()
        
        while True:
            message = input("> ")
            if message.lower() == "/view":
                self.socket.send(f"/view_chatroom_users {chatroom_name}".encode())
                response = self.socket.recv(1024).decode()
                print(response)

            if message.lower() == "/exit":
                self.socket.send(f"/exit_chatroom {chatroom_name}".encode())
                print("Exiting chatroom...")
                self.clear_terminal()
                break
            self.socket.send(f"/chatroom_message {chatroom_name} {message}".encode())
    
    """
    help_screen displays the help screen for the chat application.

    help_screen displays the help screen for the chat application, which contains information about
    the available commands and their usage. The help screen is read from a text file and displayed
    in the terminal.

    """
    def help_screen(self):
       
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
    receive_message continuously listens for messages from the server and displays them to the user.
    If the server sends an "exit" command or the connection is closed, the method terminates.
    """
    def receive_message(self):
        
        while True:
            try:
                server_message = self.socket.recv(1024).decode()
                if server_message == "exit":
                    print("You have been returned to the main menu.")
                    break
                print(server_message)
            except:
                print("Connection closed by server.")
                self.socket.close()
                break


if __name__ == '__main__':
    client = Client('127.0.0.1', 7632)