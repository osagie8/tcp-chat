import socket
from threading import Thread
import os

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Enter your name: ")
        self.socket.send(self.name.encode())
        Thread(target=self.receive_message).start()
        self.client_main_menu()

    def client_main_menu(self):
        while True:
            print("\033[1;32;40mWelcome to the chat app!\033[0m")
            print("1. Create new chatroom")
            print("2. Join existing chatroom")
            print("3. Create a Private Message")
            print("4. Exit Application")
            print("========================")

            choice = input("Enter your choice: ")

            if choice == '1':
                chatroom_name = input("Enter the name of the chat room: ")
                self.socket.send(f"/create_chatroom {chatroom_name}".encode())
                response = self.socket.recv(1024).decode()
                print(f"Server response: {response}")  # Debugging line
                if "created successfully" in response:
                    print(f"\033[1;32;40mWelcome to the chat room '{chatroom_name}'!\033[0m")
                    self.chatroom_screen(chatroom_name)
                else:
                    print("Failed to join the chat room. Server Response: "+response)

            elif choice == '2':
                chatroom_name = input("Enter the name of the chat room to join: ")
                self.socket.send(f"/join_chatroom {chatroom_name}".encode())
                response = self.socket.recv(1024).decode().strip()
                print(f"Server response: {response}")  # Debugging line
                if "Joined" in response:
                    self.clear_terminal()
                    print(f"\033[1;32;40mWelcome to the chat room '{chatroom_name}'!\033[0m")
                    self.chatroom_screen(chatroom_name)
                else:
                    print(response)
                    #print("responseresponseresponseresponseresponse")

            elif choice == '4':
                print("Exiting the application...")
                self.socket.close()
                os._exit(0)

            else:
                print("Invalid choice, please try again.")

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def chatroom_screen(self, chatroom_name):
        while True:
            message = input("")
            if message.lower() == "exit":
                self.socket.send(f"/exit_chatroom {chatroom_name}".encode())
                print("Exiting chatroom...")
                break
            self.socket.send(f"/chatroom_message {chatroom_name} {message}".encode())

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