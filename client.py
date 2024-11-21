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

def receive(sock):
    """Receive messages from the server."""
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                raise ConnectionResetError
            print(message)
        except ConnectionResetError:
            print("Disconnected from server.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    sock.close()

def send(sock):
    """Send messages to the server."""
    while True:
        try:
            message = input()
            if message.lower() == "/quit":
                print("Disconnecting from server...")
                sock.close()
                break
            sock.send(message.encode())
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
    try:
        sock.connect((host, port))
        print(f"Connected to chat server at {host}:{port}")

        # Send user name
        name = input("Enter your name: ").strip()
        sock.send(name.encode())

        receive_thread = threading.Thread(target=receive, args=(sock,))
        receive_thread.start()

        send(sock)
    except ConnectionRefusedError:
        print("Unable to connect to the server. Please check the host and port.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()


