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
import getpass # Securely prompts the user for password input
from rich import print # Enables rich text formatting for terminal output
from rich.panel import Panel # Enables rich text panel formatting for terminal output
from rich.align import Align 
from rich import print
from rich.layout import Layout
from rich.console import Console
from datetime import datetime # Handles date and time operations for message timestamps
import time # 
import NotificationHandler
from rich.table import Table


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
        self.shutdown_flag = False
        self.clear_terminal() 
        self.notifications = NotificationHandler.NotificationHandler()  # Initialize notification handler
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
            console = Console()

            # Create welcome panel
            welcome_panel = Panel(
            Align.center("[bold green]Welcome to Chitchat![/bold green]"),
            style="green",
            padding=(1,0)
            )
            console.print(welcome_panel)

            # Create authentication table
            table = Table(
            show_header=False,
            header_style="cyan",
            border_style="cyan",
            expand=True
            )
            
            #table.add_column("Option", justify="center")
            #table.add_column("", justify="center")
            
            table.add_row(
            "[green]1[/green]", 
            "[green]Login with existing account[/green]"
            )
            table.add_row(
            "[cyan]2[/cyan]", 
            "[cyan]Register new account[/cyan]"
            )
            table.add_row(
            "[red]3[/red]", 
            "[red]Exit application[/red]"
            )

            console.print(Panel(table, title="Enter an option below!", border_style="cyan"))
            
            choice = input(">> ")
            
            if choice == '1':
                self.clear_terminal()
                print(Panel.fit("[bold green]Login[/bold green]", border_style="green"))
                username = input("Username: ")
                password = getpass.getpass("Password: ")
                self.socket.send(f"/login {username} {password}".encode())
                
            elif choice == '2':
                self.clear_terminal()
                print(Panel.fit("[bold cyan]Register New Account[/bold cyan]", border_style="cyan"))
                username = input("Choose username: ")
                password = getpass.getpass("Choose Password: ")
                self.socket.send(f"/register {username} {password}".encode())
            
            elif choice == '3':
                print(Panel.fit("[bold red]Exiting...[/bold red]", border_style="red"))
                os._exit(0)
            
            else:
                print(Panel.fit("[bold red]Invalid choice[/bold red]", border_style="red"))
                continue
            
            response = self.socket.recv(1024).decode()
            if "success" in response.lower():
                self.name = username
                print(Panel.fit("[bold green]Authentication successful![/bold green]", border_style="green"))
                return
            else:
                print(Panel.fit(f"[bold red]{response}\nPlease try again[/bold red]", border_style="red"))

    """
    client_main_menu method provides the main user interface for the chat application.

    client_main_menu method provides the main user interface for the chat application, 
    displaying options such as 'Create new chatroom' or 'Join existing chatroom', 'View available chatrooms', accessing 
    help, or exiting the application. The user input and sends corresponding commands 
    to the server, and processes the server’s responses to execute the selected action.

    """    
    # MARK: Main Menu
    def client_main_menu(self):
        while not self.shutdown_flag:
            console = Console()
            layout = Layout()
            layout.split(
                Layout(name="header", size=3),
                Layout(name="body"),
                Layout(name="bottom", size=3),
            )
        
            layout["header"].split_row(
                Layout(name="left"),
                Layout(name="middle"),
                Layout(name="right"),
            )

            layout["body"].split_row(
                Layout(name="left"),
                Layout(name="right"),
            )
            layout["bottom"].split_row(
                Layout(name="one"),
            )

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            layout["header"]["left"].update(Panel(Align.center(f"User: [cyan] {self.name} [/cyan] \nTime: {current_time}"), style="green"))
            layout["header"]["middle"].update(Panel(Align.center("[bold]Main Menu[/bold]"), style="cyan"))
            layout["header"]["right"].update(Panel(Align.center("[link=https://cs-devel.potsdam.edu/S24-480-owieo204/tcp-chat]Chitchat[/link]"), style="green"))

            option_content = """
1.[cyan] Create new Chatroom[/cyan]\n
2.[cyan] Join existing Chatroom[/cyan]\n
3.[cyan] Private Messages[/cyan]\n
4.[cyan] Help[/cyan]\n
5.[cyan] Exit[/cyan]\n
       """
            layout["body"]["left"].update(Panel(option_content, title="[bold]Options[/bold]", style="green"))
        
            help_content = """[bold][cyan]Tips:[/cyan][/bold]

[cyan]-[/cyan] Use numbers 1-6 to navigate menu
[cyan]-[/cyan] Messages in chatrooms are visible to all members
[cyan]-[/cyan] Private messages are only seen by recipient
        
[cyan]Chatroom Commands:[/cyan]
[cyan]-[/cyan] [green]/view[/green] - Show users in current chatroom
[cyan]-[/cyan] [green]/exit[/green] - Leave current chatroom

[cyan]General Commands:[/cyan]
[cyan]-[/cyan] Create chatroom - Make a new chat space
[cyan]-[/cyan] Join chatroom - Enter existing chat
[cyan]-[/cyan] Private Messages - Send direct messages

        """

            layout["body"]["right"].update(Panel(help_content, title="[bold]Help Guide[/bold]", style="green"))
            layout["one"].update(Panel(Align.center(f"[dim]Connected to server: {self.socket.getpeername()[0]}:{self.socket.getpeername()[1]} [/dim]  "), style="cyan"))

            console.print(layout)   
            choice = input("") 

            if choice == '1': 
                self.clear_terminal()
                print(Panel.fit("[bold cyan]Create New Chatroom[/bold cyan]", border_style="cyan"))
                chatroom_name = input("[green]Enter chatroom name:[/green] ")
                if chatroom_name == "/exit":
                    continue
                self.socket.send(f"/create_chatroom {chatroom_name}".encode())
                response = self.socket.recv(1024).decode()
                print(response)

            elif choice == '2':
                self.clear_terminal()
                print(Panel.fit("[bold cyan]Join Existing Chatroom[/bold cyan]", border_style="cyan"))
                # First, get and display available chatrooms
                self.socket.send("/chatroom_view".encode())
                response = self.socket.recv(1024).decode()
                available_rooms = response.split(', ')
                
                if not response or response.isspace():
                    print(Panel.fit("[yellow]No chatrooms available. Create one first![/yellow]", border_style="yellow"))
                    input("\nPress Enter to return to main menu...")
                    continue
                    
                # Display available chatrooms in a formatted panel
                rooms_content = "\n".join(f"[cyan]{i+1}.[/cyan] {room}" for i, room in enumerate(available_rooms))
                print(Panel(f"Available Chatrooms:\n\n{rooms_content}", title="[bold]Select a Chatroom[/bold]", border_style="cyan"))
                
                # Get user choice
                chatroom_choice = input("\nEnter the number of the chatroom to join (or type '/exit' to return): ")
                if chatroom_choice.lower() == '/exit':
                    continue
                    
                try:
                    chatroom_index = int(chatroom_choice) - 1
                    if 0 <= chatroom_index < len(available_rooms):
                        chatroom_name = available_rooms[chatroom_index]
                        self.socket.send(f"/join_chatroom {chatroom_name}".encode())
                        response = self.socket.recv(1024).decode()
                        print(response)
                        if "Joined" in response:
                            self.chatroom_screen(chatroom_name)
                    else:
                        print(Panel.fit("[red]Invalid chatroom number[/red]", border_style="red"))
                        input("\nPress Enter to continue...")
                except ValueError:
                    print(Panel.fit("[red]Please enter a valid number[/red]", border_style="red"))
                    input("\nPress Enter to continue...")

            elif choice == '3':
                self.private_chat_screen()

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
            
            pass

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
        print(Panel.fit(f"[green]Chatroom: {chatroom_name}[/green]  |  [cyan]User: {self.name}[/cyan]", style="bold"))
        #print(f"Welcome to the chatroom {chatroom_name}! You ({self.name}), can start chatting now.")
    

        print("Type your messages below or type '/exit' to leave the chatroom.")
        print("Type '/view' to view users in chatroom.\n")
        Thread(target=self.receive_message, daemon=True).start() # Start thread to receive messages from the server
        
        while True:
            message = input("") # Chatroom message input
            # Print out own message
            print(Panel(f"[cyan]{self.name}[/cyan]: {message}", style="cyan", width=60)) 

            if message.lower() == "/view": 
                self.socket.send(f"/view_chatroom_users {chatroom_name}".encode()) # Send request to view chatroom users
                response = self.socket.recv(1024).decode()
                print(response)
                print("\nContinue chatting below or type '/exit' to leave the chatroom.")
                continue  # Continue the chat loop after showing users

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

        help_content = """
        [cyan]Welcome to ChitChat![/cyan]
        A real-time chat application for connecting with others.

        [cyan]Navigation Tips:[/cyan]
        - Use numbers [green]1-6[/green] to navigate the main menu
        - Press [green]Enter[/green] to confirm your selections
        - Type [green]/exit[/green] to return to previous menu

        [cyan]Chatroom Features:[/cyan]
        - [green]Create Chatroom[/green]: Start your own chat space
        - [green]Join Chatroom[/green]: Enter existing chatrooms
        - [green]Private Messages[/green]: Send direct messages to users

        [cyan]Chatroom Commands:[/cyan]
        - [green]/view[/green] - Show all users in current chatroom
        - [green]/exit[/green] - Leave current chatroom

        [cyan]Private Messaging:[/cyan]
        - Send private messages to specific users
        - View your message history
        - Mark messages as read/unread
        """

        Help_panel = Panel(f"[bold blue]{help_content}[/bold blue]\n", title="Help", border_style="cyan")    
        print(Help_panel)

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
        
        while not self.shutdown_flag:
            try:
                server_message = self.socket.recv(1024).decode()
                
                # Handle server exit message
                if server_message == "exit":
                    print("You have been returned to the main menu.")
                    break
                    
                # Handle notification commands from server
                if server_message.startswith("/notification"):
                    _, notification_msg = server_message.split(" ", 1)
                    self.notifications.notify_unread_messages(
                        int(''.join(filter(str.isdigit, notification_msg)))
                    )
                    continue
                    
                # Handle private messages
                if server_message.startswith("[Private from"):
                    sender = server_message[12:].split("]")[0].strip()
                    message = server_message.split("]: ")[1]
                    self.notifications.notify_private_message(sender, message)

                if server_message.startswith("Server is shutting down..."):
                    print(Panel.fit("[bold red]Server is shutting down...[/bold red]", border_style="red"))
                    self.shutdown_flag = True
                    try:
                        self.socket.send("/exit".encode())
                    except:
                        pass
                    finally:
                        self.socket.close()
                    break 
                
                
                # Handle regular chatroom messages
                elif ":" in server_message:
                    try:
                        sender = server_message.split(":")[0].strip().replace("[bold blue]", "").replace("[/bold blue]", "")
                        message = ":".join(server_message.split(":")[1:]).strip()
                        if sender != self.name:  # Don't notify for own messages
                            self.notifications.notify_new_message(sender, message)
                    except IndexError:
                        pass  # Malformed message, skip notification
                
                # Display the message
                current_time = datetime.now().strftime("%H:%M")
                print(Panel(f"[cyan]{current_time}[/cyan] {server_message}", 
                        style="green", width=60))
                        
            except Exception as e:
                print(f"Connection closed by server: {e}")
                self.socket.close()
                break

    """
    private_chat_screen - Shows private messaging menu interface
    
    private_chat_screen displays the main private messaging menu with options to
    view inbox, send new messages, or return to main menu. Handles user input
    and navigation between private messaging functions.
    
    @param self: Client instance
    """
    def private_chat_screen(self):
        while True:
            self.clear_terminal()
            console = Console()

            # Create header panel
            header_panel = Panel(
                Align.center("[bold cyan]Private Messages[/bold cyan]"),
                style="cyan",
                padding=(1,0)
            )
            console.print(header_panel)

            # Create options table
            table = Table(
                show_header=False,
                header_style="cyan",
                border_style="cyan",
                expand=True
            )
            
            table.add_row(
                "[green]1[/green]",
                "[green]View Inbox[/green]"
            )
            table.add_row(
                "[cyan]2[/cyan]",
                "[cyan]Send New Message[/cyan]" 
            )
            table.add_row(
                "[red]3[/red]",
                "[red]Return to Main Menu[/red]"
            )

            console.print(Panel(table, title="Select an option:", border_style="cyan"))
            
            choice = input(">> ")
            
            if choice == '1':
                self.view_inbox()
            elif choice == '2':
                self.send_private_message()
            elif choice == '3':
                self.clear_terminal()
                break
            else:
                print(Panel.fit("[bold red]Invalid choice[/bold red]", border_style="red"))
                time.sleep(1)

    """
    view_inbox - Displays user's private message inbox
    
    view_inbox retrieves and displays all private messages for the current user
    with sender info, timestamp, and read status. Allows marking unread messages
    as read and navigating message history.
    
    @param self: Client instance
    """
    def view_inbox(self):
        self.clear_terminal()
        print(Panel.fit("[bold cyan]Inbox[/bold cyan]", border_style="green"))
        
        self.socket.send("/get_messages".encode())
        response = self.socket.recv(1024).decode()
        
        try:
            messages = eval(response)  # Convert string representation back to list
            if not messages:
                print(Panel("No messages in inbox.", style="yellow"))
                input("\nPress Enter to return to private chat menu...")
                return

            # Display messages in a panel   
            for msg in messages:
                sender, content, timestamp, msg_id, status = msg
                status_color = "red" if status == "Unread" else "green"
                
                message_panel = Panel(
                    f"[bold blue]From:[/bold blue] {sender}\n"
                    f"[bold blue]Time:[/bold blue] {timestamp}\n"
                    f"[bold blue]Status:[/bold blue] [{status_color}]{status}[/{status_color}]\n"
                    f"[bold blue]Message:[/bold blue] {content}",
                    title=f"Message ID:{msg_id}",
                    border_style="cyan"
                )
                print(message_panel)
                
                # Mark as read option
                if status == 'Unread':
                    if input("\nMark as read? (y/n): ").lower() == 'y':
                        self.socket.send(f"/mark_read {msg_id}".encode())
                        self.socket.recv(1024)  # Get confirmation
                        print("[green]Message marked as read![/green]")
                print() 
                
        except Exception as e:
            print(Panel(f"[red]Error displaying messages: {str(e)}[/red]", style="red"))
        
        input("\nPress Enter to return to private chat menu...")
        self.clear_terminal()

    """
    send_private_message - Handles sending new private messages
    
    send_private_message prompts user for recipient and message content, validates
    input, sends message to server, and displays confirmation or error response.
    Handles all UI aspects of composing and sending private messages.
    
    @param self: Client instance
    """
    def send_private_message(self):
        self.clear_terminal()
        
        # Display header
        print(Panel.fit("[bold cyan]Send Private Message[/bold cyan]", border_style="cyan"))
        
        # Get recipient and message with styled prompts
        recipient = input("\nEnter recipient's username: ")
        if not recipient:
            print(Panel("[red]Recipient username cannot be empty[/red]", border_style="red"))
            input("\nPress Enter to try again...")
            return
            
        message = input("Enter your message: ")
        if not message:
            print(Panel("[red]Message cannot be empty[/red]", border_style="red"))
            input("\nPress Enter to try again...")
            return
        
        # Send message to server
        self.socket.send(f"/send_private {recipient} {message}".encode())
        response = self.socket.recv(1024).decode()
        
        # Display response in a panel
        if "success" in response.lower():
            print(Panel(f"[green]{response}[/green]", border_style="green"))
        else:
            print(Panel(f"[red]{response}[/red]", border_style="red"))
        
        input("\n[dim]Press Enter to return to private chat menu...[/dim]")
        self.clear_terminal()

    
if __name__ == '__main__':
    client = Client('127.0.0.1', 7632) # Initialize client with server IP and port