import socket
from threading import Thread
# Provides us with methods for interacting with the operating system.
import os

class Client:
  
  # Client Contructor Connects to the server, ask for
  # a username, and begin server communication.
  def __init__(self, HOST, PORT):
    self.socket = socket.socket()
    self.socket.connect((HOST, PORT))
    self.name = input("Enter your name: ")
    #print("\n" + "\033[1;32;40m" + "Your User ID is: " + self.socket.recv(1024).decode() + "\033[0m")

    self.talk_to_server()
  
  def client_main_menu(client):
    while True:
        print("\033[1;32;40m" + "Welcome to the chat app!" + "\033[0m")
        
        print("1. Create new chat room")
        print("2. Join existing chat room")
        print("3. Create a Private Message")
        print("4. Help")

        print("5. Exit Application")
       
        print("========================")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            chatroom_name = input("Enter the name of the chat room: ")
            client.socket.send(f"/create_chatroom {chatroom_name}".encode())
            response = client.socket.recv(1024).decode()
            print(response)
            
        elif choice == '5':
            print("Exiting the chat...")
            client.socket.close()
            os._exit(0)    
        else:
            print("Invalid choice, please try again.")  

 
  def talk_to_server(self):
    # Send over the name of the client. 
    self.socket.send(self.name.encode())
    # Then start listening for messages on a separate thread.
    Thread(target = self.receive_message).start()
    self.client_main_menu()
    self.send_message()
    
    
  # Get user input and send the message to the server
  # with the client's name prepended.
  def send_message(self):
    while True:
      client_input = input("")
      if client_input.strip().lower() == "/exit":
                print("Exiting the chat...")
                self.socket.close()
                os._exit(0)
      client_message = self.name + ": " + client_input
      self.socket.send(client_message.encode())
      
  # Constantly listen out for messages. If the message is response
  # from the server is empty, close the program.
  def receive_message(self):
    while True:
      server_message = self.socket.recv(1024).decode()
      if not server_message.strip():
        os._exit(0)
 
      print("\n" + "\033[1;32;40m" + "User ID " + server_message + "\033[0m")
      
if __name__ == '__main__':
  client = Client('127.0.0.1', 7632)
  client.client_main_menu(client)