
 * author: Osagie Owie
 * email: owieo204@potsdam.edu
 * course: CIS 480 Senior Project
 * assignment: Senior Project
 * due 3/1/25 

# TCP Chat Application - ChitChat
# Table of Contents

- [TCP Chat Application](#tcp-chat-application)
  - [Features](#features)
  - [How to Run + Environment Setup](#how-to-run--environment-setup)
  - [Project Structure](#project-structure)
  - [Usage Guide](#usage-guide)
    - [Starting the Server](#starting-the-server)
    - [Running a Client](#running-a-client)
    - [Client Commands](#client-commands)
  - [Technology Stack](#technology-stack)
  - [Documentation](/Documentation/documentation.md)

## Description
ChitChat is a TCP-based chat application enabling real-time communication between multiple clients through a central server. This application features a command-line interface, supports group chats, and includes user authentication with secure password management.

## [Documentation can be found here.](/Documentation/documentation.md)


## Features
- **Server Features**:
  - Authentication & User Management
    - User Registration System
    - Login System
    - Client Connection Management
  - Chatroom Management
    - Chatroom Creation
    - Chatroom Administration
    - Message Handling
  - Database Management
    - User Data
    - Chatroom Data
    - Message Data
  - Server Administration
    - Server Control
    - Error Handling

- **Client Features**:
  - User Interface
    - Main Menu
    - Authentication Interface
    - Chatroom Interface
  - Command System
    - General Commands
    - Chatroom Commands
  - Connection Management
    - Server Communication
    - Message Handling
  - User Experience
    - Navigation 
    - Error Handling
  - Session Management
    - User Session
    - Chatroom Session

## How to Run + Environment Setup
1. Clone the repository:
   ```bash 
   git clone https://cs-devel.potsdam.edu/S24-480-owieo204/tcp-chat.git
   cd tcp-chat/src

2. Create the virtual environment:
   ```bash 
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

## Project Structure
```
tcp-chat/src
│
├── server.py           # Server implementation
├── client.py           # Client implementation
├── requirements.txt    # Project dependencies
├── help.txt           # Help documentation
└── chat_app.db        # SQLite database
```
## [Documentation can be found here.](/Documentation/documentation.md)

## Usage Guide 
GIFS coming soon*

### Starting the Server

1. Activate the virtual environment (if not already activated)
2. Start the server:
   ```bash
   python3 server.py
   ```
3. The server will start listening on localhost (127.0.0.1) port 7632

### Running a Client

1. Open a new terminal window
2. Activate the virtual environment
3. Start the client:
   ```bash
   python3 client.py
   ```

### Client Commands

After connecting, you can: 

1. **Register/Login**
   - Choose to register a new account or login
   - Usernames must be unique
   - Passwords must be at least 8 characters

2. **Main Menu Options**
   - Create new chatroom: Create a custom chatroom where you can chat with other users. You'll be prompted to provide a name for your chatroom.
   - Join existing chatroom: Connect to an already created chatroom by entering its name. You can then participate in group conversations with other members.
    - While user is in chatroom, they are able to send messages to the chat room. Type /view to view connected users in chatrooms and type /exit to leave the chat room.
   - View available chatrooms: See a list of all currently active chatrooms that you can join.
   - Access help: View detailed instructions and commands available in the application.
   - Exit application: Safely disconnect from the server and close the application.

## Technology Stack
- **Programming Language**: Python3
- **Libraries**: `socket`, `threading`, `sqlite3`, `bcrypt`, `os`, `Rich`

## [Documentation can be found here.](/Documentation/documentation.md)







