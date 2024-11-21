'''
server.py is the Server for the TCP chat application.

  @author Osagie Owie
  @email owieo204@potsdam.edu
  @course CIS 480 Senior Project
  @assignment: Senior Project
  @due 12/9/24 
 '''

import socket
import threading
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def broadcast(message, sender, clients, lock):
    """Broadcast message to all clients except the sender."""
    with lock:
        for client, name in clients.items():
            if client != sender:
                try:
                    client.send(message.encode())
                except Exception as e:
                    logging.error(f"Error broadcasting message: {e}")
                    client.close()
                    del clients[client]

def handle_client(client, address, clients, lock):
    """Handle communication with a single client."""
    logging.info(f"Handling client {address}")
    try:
        # Ask for the client's name
        client.send("Enter your name: ".encode())
        name = client.recv(1024).decode().strip()
        if not name:
            name = f"Client-{address[1]}"  # Default name if none provided

        # Add client to the list
        with lock:
            clients[client] = name

        welcome_message = f"{name} has joined the chat!"
        logging.info(welcome_message)
        broadcast(welcome_message, client, clients, lock)

        # Handle incoming messages
        while True:
            message = client.recv(1024).decode()
            if not message:
                raise ConnectionResetError
            formatted_message = f"{name}: {message}"
            logging.info(formatted_message)
            broadcast(formatted_message, client, clients, lock)
    except ConnectionResetError:
        logging.info(f"{clients.get(client, 'Unknown Client')} disconnected")
    except Exception as e:
        logging.error(f"Error with client {address}: {e}")
    finally:
        # Clean up on disconnection
        with lock:
            if client in clients:
                disconnected_name = clients[client]
                del clients[client]
                broadcast(f"{disconnected_name} has left the chat.", client, clients, lock)
        client.close()

def main():
    """Main server function."""
    parser = argparse.ArgumentParser(description="TCP Chat Server")
    parser.add_argument("--host", default="127.0.0.1", help="Server IP address")
    parser.add_argument("--port", type=int, default=9090, help="Server port")
    args = parser.parse_args()

    host, port = args.host, args.port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    logging.info(f"Server started on {host}:{port}")

    clients = {}  # Store clients as {socket: name}
    lock = threading.Lock()

    try:
        while True:
            client, address = server_socket.accept()
            logging.info(f"New connection from {address}")
            thread = threading.Thread(target=handle_client, args=(client, address, clients, lock))
            thread.start()
    except KeyboardInterrupt:
        logging.info("Shutting down the server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
