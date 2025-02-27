"""
stress_test.py - A simple stress testing utility for the ChitChat application

This script simulates multiple clients connecting to the chat server simultaneously
and sending messages to test server performance and stability under load.

Usage: python stress_test.py [OPTIONS]
Options:
  --host HOST         Server host address (default: 127.0.0.1)
  --port PORT         Server port (default: 7632)
  --clients NUM       Number of simultaneous clients (default: 10)
  --messages NUM      Number of messages per client (default: 5)
  --interval SECONDS  Delay between messages (default: 0.5)
  --chatroom NAME     Chatroom name to use (default: "StressTest")
"""

import socket
import threading
import time
import random
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

class TestClient:
    """Simulates a client connection to the chat server."""
    
    def __init__(self, host, port, client_id, messages, interval, chatroom):
        """Initialize test client with connection parameters."""
        self.host = host
        self.port = port
        self.client_id = client_id
        self.username = f"test_user_{client_id}"
        self.password = f"password{client_id}"
        self.messages = messages
        self.interval = interval
        self.chatroom = chatroom
        self.socket = None
        
    def connect(self):
        """Establish connection to the server and authenticate."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Client {self.client_id}: Connected to server")
            
            # Register the user
            self.socket.send(f"/register {self.username} {self.password}".encode())
            response = self.socket.recv(1024).decode()
            
            # If registration fails (likely because user exists), try to login
            if "successful" not in response.lower():
                self.socket.send(f"/login {self.username} {self.password}".encode())
                response = self.socket.recv(1024).decode()
                
            if "successful" not in response.lower():
                print(f"Client {self.client_id}: Authentication failed - {response}")
                self.socket.close()
                return False
                
            print(f"Client {self.client_id}: Authentication successful")
            return True
            
        except Exception as e:
            print(f"Client {self.client_id}: Connection error - {str(e)}")
            if self.socket:
                self.socket.close()
            return False
            
    def join_or_create_chatroom(self):
        """Join the specified chatroom or create it if it doesn't exist."""
        try:
            # First try to join the chatroom
            self.socket.send(f"/join_chatroom {self.chatroom}".encode())
            response = self.socket.recv(1024).decode()
            
            # If joining fails, create the chatroom
            if "joined" not in response.lower():
                self.socket.send(f"/create_chatroom {self.chatroom}".encode())
                response = self.socket.recv(1024).decode()
                
                if "created" not in response.lower():
                    print(f"Client {self.client_id}: Failed to create/join chatroom - {response}")
                    return False
                    
                # Try joining again after creating
                self.socket.send(f"/join_chatroom {self.chatroom}".encode())
                response = self.socket.recv(1024).decode()
                
            print(f"Client {self.client_id}: Joined chatroom {self.chatroom}")
            
            # Start a thread to receive messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Client {self.client_id}: Error joining chatroom - {str(e)}")
            return False
            
    def receive_messages(self):
        """Listen for and handle incoming messages from the server."""
        try:
            while True:
                response = self.socket.recv(1024).decode()
                if not response:
                    break
                # Just a minimal handler for server responses
                if "exit" in response.lower():
                    break
        except:
            pass
            
    def send_messages(self):
        """Send a series of test messages to the chatroom."""
        try:
            for i in range(self.messages):
                message = f"Test message {i+1} from client {self.client_id} at {time.time()}"
                self.socket.send(f"/chatroom_message {self.chatroom} {message}".encode())
                print(f"Client {self.client_id}: Sent message {i+1}/{self.messages}")
                time.sleep(self.interval)
                
            # Exit the chatroom
            self.socket.send(f"/exit_chatroom {self.chatroom}".encode())
            time.sleep(0.5)  # Wait for exit confirmation
            
            return True
            
        except Exception as e:
            print(f"Client {self.client_id}: Error sending messages - {str(e)}")
            return False
            
    def disconnect(self):
        """Close the connection to the server."""
        try:
            if self.socket:
                self.socket.send("/exit".encode())
                self.socket.close()
                print(f"Client {self.client_id}: Disconnected from server")
        except:
            pass
            
    def run(self):
        """Execute the complete test sequence for this client."""
        success = self.connect()
        if not success:
            return False
            
        success = self.join_or_create_chatroom()
        if not success:
            self.disconnect()
            return False
            
        success = self.send_messages()
        self.disconnect()
        return success

def run_stress_test(args):
    """Execute the stress test with multiple clients."""
    print(f"\n===== Starting Stress Test with {args.clients} clients =====")
    print(f"Server: {args.host}:{args.port}")
    print(f"Messages per client: {args.messages}")
    print(f"Interval between messages: {args.interval} seconds")
    print(f"Chatroom: {args.chatroom}\n")
    
    start_time = time.time()
    success_count = 0
    
    # Create and run clients in parallel using a thread pool
    with ThreadPoolExecutor(max_workers=args.clients) as executor:
        futures = []
        for i in range(args.clients):
            client = TestClient(
                args.host, 
                args.port, 
                i+1, 
                args.messages, 
                args.interval, 
                args.chatroom
            )
            futures.append(executor.submit(client.run))
            
            # Small delay between client starts to avoid connection flood
            time.sleep(0.2)
            
        # Wait for all clients to complete
        for future in futures:
            if future.result():
                success_count += 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Calculate statistics
    total_messages = args.clients * args.messages
    messages_per_second = total_messages / duration if duration > 0 else 0
    
    print("\n===== Stress Test Results =====")
    print(f"Total test duration: {duration:.2f} seconds")
    print(f"Successful clients: {success_count}/{args.clients}")
    print(f"Total messages sent: {total_messages}")
    print(f"Messages per second: {messages_per_second:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stress test the ChitChat server")
    parser.add_argument("--host", default="127.0.0.1", help="Server host address")
    parser.add_argument("--port", type=int, default=7632, help="Server port")
    parser.add_argument("--clients", type=int, default=10, help="Number of simultaneous clients")
    parser.add_argument("--messages", type=int, default=5, help="Messages per client")
    parser.add_argument("--interval", type=float, default=0.5, help="Delay between messages (seconds)")
    parser.add_argument("--chatroom", default="StressTest", help="Chatroom name to use")
    
    args = parser.parse_args()
    
    try:
        run_stress_test(args)
    except KeyboardInterrupt:
        print("\nStress test interrupted by user")
    except Exception as e:
        print(f"\nError during stress test: {str(e)}")
    
    print("\nStress test completed")
