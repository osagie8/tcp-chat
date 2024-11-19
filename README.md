
 * author: Osagie Owie
 * email: owieo204@potsdam.edu
 * course: CIS 480 Senior Project
 * assignment: Senior Project
 * due 12/9/24 


# TCP Chat Application

## Description
This project is a TCP-based chat application for real-time communication between multiple clients connected to a central/main server. It offers a command-line interface alongside a graphical user interface (GUI), supports private and broadcast messaging, file sharing, and seamless reconnection for disconnected clients.

## Features
- **Server Features**:
  - User authentication.
  - Client management with unique identifiers.
  - Broadcast, private, and group messaging.
  - File sharing with bandwidth management.

- **Client Features**:
  - Command-line and GUI-based interfaces.
  - Real-time message sending and receiving.
  - Notifications for new messages and connection status.

## Technology Stack
- **Programming Language**: Python
- **Libraries**: `socket`, `threading`, `tkinter`

## How to Run + Environment Setup
1. Clone the repository:
   ```bash 
   git clone https://cs-devel.potsdam.edu/S24-480-owieo204/tcp-chat.git

- Since we are using one machine for now, create 3 different terminal sessions to simulate 3 connected machines .

2. Run server.py
    ```bash
    python server.py

3. Run client.py
    ```bash
    python client.py

4. Run gclient.py
    ```bash
    python gclient.py

## Program Execution Instructions

1.  Write text in client.py CLI and it will broadcast to any other client that is is our server.
2.  Write text in the gclient.py GUI and it will broadcast to any other client that is is our server.

## Testing

- Program was tested on one machine. I intend to test it out with multiple machines.
- 


