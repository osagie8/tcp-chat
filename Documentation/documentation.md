# Documentation
## Overview
The chat application enables real-time communication between multiple clients through a central server. It features user authentication, chatroom management, and message persistence using SQLite. The application implements a multi-threaded architecture to handle concurrent connections efficiently.

## Quick Start Guide

### Environment Setup
```bash
# Clone the repository
git clone https://cs-devel.potsdam.edu/S24-480-owieo204/tcp-chat.git

# Activate virtual environment
source venv/bin/activate  # Unix/MacOS
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
1. Start the server:
```bash
python3 server.py
```

2. Start the client(s):
```bash
python3 client.py 
```

3. Register or login when prompted.

# Table of Contents
## [1. High-Level Architecture](#high-level-architecture)
## [2. Component Breakdown](#component-breakdown)
## [3. Data Flow](#data-flow)
## [4. Technical Benefits](#technical-benefits)
## [5. Implementation Details](#Communication-Implementation)
## [6. Database Schema](#database-schema)
## [7. Testing](#Testing)
## [8. Acknowledgments and References](#acknowledgments-and-references)

## High-Level Architecture

```
[Client Layer]
    │
    |
[Transport Layer (TCP/IP)]
    │
    |
[Server Layer]
    │
    |
[Database Layer]
```

## Component Breakdown

- The application is divided into the Client Layer (`client.py`) which handles user interaction and server communication, the Transport Layer which uses Python's `socket` library for TCP/IP communication, the Server Layer (`server.py`) which manages client connections, message routing, and chatroom logic, and the Database Layer (SQLite) which stores user accounts, chat history, and chatroom data.

### 1. Client Layer (`client.py`)

- Handles user interface and interaction
    - Provides clean command-line interface with menus
    - Handles user input
    - Displays system messages and responses
    - Manages application navigation
- Manages connection to server
    - Creates TCP socket connection to server
    - Handles connection initialization and cleanup
- Processes incoming/outgoing messages
    - Sends commands and messages to server
    - Receives and displays incoming messages
    - Handles message encoding/decoding

### 2. Transport Layer

- The transport layer is handled through Python's `socket` library implementing TCP/IP
    - Server uses `AF_INET` (IPv4) and `SOCK_STREAM` (TCP) for reliable, ordered communication.

- Uses TCP/IP for reliable communication
- Ensures message delivery and ordering

### 3. Server Layer (`server.py`)

- Manages client connections
    - Tracks active client connections in the clients list
    - Handles new client connections and disconnections
    - Manages client state
    - Provides clean disconnection 
- Routes messages between clients
    - Handles different message types (chatroom, private)
    - Ensures message delivery to correct clients
    - Manages message broadcasting in chatrooms
- Handles chatroom logic
    - Maintains active chatrooms in chatrooms dictionary
    - Handles chatroom creation and deletion
    - Manages user membership in chatrooms
- Authenticates users
    - Verifies user credentials against database
    - Handles user registration and login
    - Manages user authentication state

### 4. Database Layer (SQLite)
- Stores user accounts
    - Securely stores usernames and hashed passwords
    - Manages user authentication data
    - Handles user registration and login
    - Ensures username uniqueness
- Persists chat history
    - Records all chat messages with timestamps
    - Stores message metadata (sender, chatroom)
    - Enables message retrieval and history viewing
- Maintains chatroom data
    - Tracks chatroom ownership/admin status
    - Maintains member lists
- Handles data relationships
    - Manages user-chatroom memberships
    - Handles message-chatroom associations
    - Links users to their messages


### 4. Security Feautures
- Password Hashing with bcrypt
- Error Handling
---

## Data Flow 
Visuals to be made***
### Authentication Flow ###

```
Client to Server: /login or /register command
Server to Database: Verify/store credentials
Database to Server: Confirmation
Server to Client: Success/failure response
```
### Message Flow ###

```
Client 'A' to Server: Send message
Server to Database: Store message
Server to Client 'B': Forward message
```
### Chatroom Flow ###

```
Client to Server: Create/join room
Server to Database: Update room data
Server to Other Clients: Room updates
```
---

## Technical Benefits

### Thread Management ###

```python
Thread(target=self.handle_client).start()
```
- Non-blocking operations
    - The server can handle multiple clients simultaneously without waiting for each operation to complete
- Concurrent client handling
    - Multiple clients can connect and communicate simultaneously
    - Server uses a dedicated thread per client for message handling
    - Thread isolation prevents issues in one client from affecting others
    - The server can scale to handle multiple connections efficiently
- Responsive user interface
    - Message receiving runs in a background thread, allowing continuous UI interaction
    - Users can type messages while simultaneously receiving them
    - The interface remains responsive even during network operations

### SQLite Integration ###

```python
conn = sqlite3.connect('chat_app.db')
```
- Built-in database
    - No separate installation required
    - Database stored in single file 'chat_app.db'
    - Easy backup and portability
    - Zero-configuration setup
- No separate server needed
    - Direct file access for operations

## Communication Implementation

The application utilizes Python's `socket` library for TCP/IP networking, implementing a client-server architecture:

### Server Side `server.py`
- Binds to specified host/port and listens for incoming connections
- Uses multi-threading to handle concurrent client connections
- Each client connection gets dedicated thread via `Thread(target=self.handle_client)`

### Client Side `client.py`
- Connects directly to server via TCP sockets
- Maintains persistent connection for real-time messaging
- Uses separate threads for receiving messages and user interface

### Threading Architecture
- Separate threads for:
  - Server menu management
  - Client message handling
  - Message receiving
- Daemon threads used for background tasks
- Enables concurrent processing of multiple client connections

## Message Handling

### Command Protocol

The expected commands from the client to server include:

```
/register <username> <password> - User registration
/login <username> <password> - Authentication
/create_chatroom <name> - Create new chatroom
/join_chatroom <name> - Join existing chatroom
/chatroom_message <room> <message> - Send message
/view_chatroom_users <room> - List room members
```

### Message Broadcasting
- Messages are broadcast to relevant chatroom members through socket connections
- Server handles routing of messages to appropriate recipients
- Disconnection handling removes clients from tracked collections

## Authentication & Session Management
1. Client must authenticate before accessing features
2. Successful authentication stores username in server's client_info
3. Session persists until client disconnects or server shuts down

## Database Schema

The application uses SQLite with the following schema:

### Users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL            
)
```
- The users table is the foundation of user authentication and identity management.
    - Ensures each user has a unique username
    - Stores passwords securely using hashing and salting
    - Provides reference point for user-related operations
    - Enables user authentication and session management

### Chatrooms Table
```sql
CREATE TABLE chatrooms (
    chatroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    admin_id INTEGER,
    FOREIGN KEY (admin_id) REFERENCES users (user_id)
)
```
- The chatrooms table manages the creation and configuration of chat spaces.
    - Maintains list of available chat rooms
    - Tracks ownership through admin relationship
    - Ensures unique chatroom names

### Chatroom Members Table
```sql
CREATE TABLE chatroom_members (
    chatroom_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (chatroom_id, user_id),
    FOREIGN KEY (chatroom_id) REFERENCES chatrooms (chatroom_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
```
- The chatroom_members table manages user participation in chatrooms.
    - Implements many-to-many relationship between users and chatrooms
    - Tracks current members of each chatroom
    - Enables access control to chatroom messages
    - Facilitates member list queries

### Messages Table

```sql
CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chatroom_id INTEGER,
    user_id INTEGER,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chatroom_id) REFERENCES chatrooms (chatroom_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
```
- The messages table preserves the chat history and enables message retrieval.
    - Stores all chat messages with metadata
    - Maintains chronological order via timestamps
    - Links messages to their senders and chatrooms
    - Enables message history queries

### Database Relationships
- One-to-many between users and messages
    - One user can send many messages
    - Each message belongs to exactly one user
    - Implemented through user_id foreign key in messages table
- Many-to-many between users and chatrooms through chatroom_members
    - Users can be members of multiple chatrooms
    - Chatrooms can have multiple users
    - Implemented through chatroom_members junction table
- One-to-many between chatrooms and messages
    - One chatroom can contain many messages
    - Each message belongs to exactly one chatroom
    - Implemented through chatroom_id foreign key in messages table
- One-to-one between chatrooms and admin users
    - Each chatroom has exactly one admin user
    - Users can be admin of multiple chatrooms
    - Implemented through admin_id foreign key in chatrooms table

---

# Testing
### Test Categories
1. Connection Management
   - Server startup
   - Client connection/disconnection
   - Concurrent client handling

2. Authentication
   - User registration
   - Login validation
   - Password security

3. Message Routing
   - Chatroom message delivery
   - Private messaging
   - Broadcast messages

4. Database Operations
   - Data persistence
   - Transaction integrity
   - Concurrent access

## Known Issues 
- Client disconnection tracking needs improvement
- Limited to local network deployment
- Basic error recovery mechanisms

## Future Enhancements

---

### More work on documentation to be done...

---

# Acknowledgments and References

## Learning Resources

- **Python Socket Programming Documentation**
  - Official Python Documentation
  - https://docs.python.org/3/library/socket.html
  - Used for understanding TCP socket implementation and network programming concepts

- **SQLite Documentation**
  - SQLite Official Documentation
  - https://sqlite.org/docs.html
  - Referenced for database design and implementation

## Open Source Libraries

- **Rich**
  - Version: [4.0.1]
  - https://github.com/
  - Used for 

- **bcrypt**
  - Version: [4.0.1]
  - https://github.com/pyca/bcrypt
  - Used for secure password hashing

- **threading**
  - Python Standard Library
  - Used for implementing concurrent operations

## Tutorials and Guides

- **Real Python**
  - "Socket Programming in Python"
  - https://realpython.com/python-sockets/
  - Helped with understanding socket programming fundamentals

- **Python Socket Programming Tutorials**
  - Python Socket Programming Tutorial for Beginners
  - https://www.youtube.com/watch?v=7gek0eCnbHs&t=944s
  - Helped with understanding socket programming fundamentals

- **Python SQLite3 Tutorial**
  - Official Python Documentation
  - https://docs.python.org/3/library/sqlite3.html
  - Referenced for database operations
  
- **WittCode Blog**
  - "Python Socket Programming Multiple Clients Chat"
  - https://blog.wittcode.com/blogs/python-socket-programming-multiple-clients-chat
  - Referenced for multi-client chat implementation concepts

## Code Attribution and Inspirations

This project was inspired by and references concepts from several open-source projects:

- **BasharAZ1 Chat App**
  - https://github.com/BasharAZ1/Chat-app-using-socket
  - Inspired socket programming structure and client handling

- **Nishi719 Chat Application**
  - https://github.com/nishi719/Chat-Application-Using-Socket-Programming
  - Referenced for server implementation patterns

