'''
client.py is the user interface for the TCP chat application on the command line.

  @author Osagie Owie
  @email owieo204@potsdam.edu
  @course CIS 480 Senior Project
  @assignment: Senior Project
  @due 12/9/24 
 '''

import socket
import threading

# Server connection settings
HOST = "127.0.0.1"
PORT = 9090

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = sock.recv(1024).decode()
            print(message)
        except:
            print("An error occurred!")
            sock.close()
            break

# Function to send messages to the server
def send():
    while True:
        message = input()
    