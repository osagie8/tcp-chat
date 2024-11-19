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
        sock.send(message.encode())

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()


