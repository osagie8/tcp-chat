'''
gclient.py is the user interface for the TCP chat application with a GUI.

  @author Osagie Owie
  @email owieo204@potsdam.edu
  @course CIS 480 Senior Project
  @assignment: Senior Project
  @due 12/9/24 
 '''

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

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
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, message + '\n')
            chat_area.yview(tk.END)
            chat_area.config(state=tk.DISABLED)
        except:
            messagebox.showerror("Error", "An error occurred!")
            sock.close()
            break

# Function to send messages to the server
def send():
    message = message_entry.get()
    if message:
        sock.send(message.encode())
        message_entry.delete(0, tk.END)

# Function to close the application
def on_closing():
    sock.close()
    window.quit()

# Create the GUI
window = tk.Tk()
window.title("TCP Chat Room Client")

# Chat area (for displaying messages)
chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED)
chat_area.pack(padx=20, pady=5, expand=True, fill=tk.BOTH)

# Message entry box
message_entry = tk.Entry(window)
message_entry.pack(padx=20, pady=5, fill=tk.X)

# Send button
send_button = tk.Button(window, text="Send", command=send)
send_button.pack(padx=20, pady=5)

# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Handle window close event
window.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI event loop
window.mainloop()
