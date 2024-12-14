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
import argparse

def receive(sock, is_active):
    """Receive messages from the server."""
    while is_active[0]:
        try:
            message = sock.recv(1024).decode()
            if not message:
                print("Server closed the connection.")
                break
            print(message)
        except ConnectionResetError:
            print("Disconnected from server.")
            break
        except OSError:
            # This occurs when the socket is already closed
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    is_active[0] = False  # Signal to stop other thread

def send(sock, is_active):
    """Send messages to the server."""
    while is_active[0]:
        try:
            message = input()
            if message.lower() == "/quit":
                print("Disconnecting from server...")
                is_active[0] = False  # Signal to stop other thread
                break
            sock.send(message.encode())
        except OSError:
            # This occurs when the socket is already closed
            break
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def main():
    parser = argparse.ArgumentParser(description="TCP Chat Client")
    parser.add_argument("--host", default="127.0.0.1", help="Server IP address")
    parser.add_argument("--port", type=int, default=9090, help="Server port")
    args = parser.parse_args()

    host, port = args.host, args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_active = [True]  # Shared state to manage socket activity across threads

    try:
        sock.connect((host, port))
        print(f"Connected to chat server at {host}:{port}")

        # Send user name
        name = input("Enter your name: ").strip()
        sock.send(name.encode())

        # Start threads
        receive_thread = threading.Thread(target=receive, args=(sock, is_active))
        receive_thread.start()

        send(sock, is_active)  # Runs in the main thread
    except ConnectionRefusedError:
        print("Unable to connect to the server. Please check the host and port.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        is_active[0] = False  # Ensure all threads stop
        try:
            sock.close()  # Safely close the socket
        except OSError:
            pass  # Ignore if socket is already closed
        print("Client closed.")

if __name__ == "__main__":
    main()
