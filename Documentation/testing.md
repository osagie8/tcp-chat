# Testing Documentation

## Test Environment Setup

### Prerequisites
- Python virtual environment with all dependencies installed
- SQLite database initialized

### Test Configuration
- Host: 127.0.0.1 (localhost)
- Port: 7632
- Local dev environment (Python 3.11, SQLite)

---
**Title**: User Registration Flow
**Description**: Verify new user registration process with valid credentials

Steps to Reproduce:
1. Start server
2. Connect client
3. Select registration option
4. Enter new username/password
   
**Expected Result**: User successfully registered in database
**Actual Result**: User successfully registered in database
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: High
**Status**: Done

---

**Title**: Duplicate Username Prevention
**Description**: System should prevent duplicate username registration

Steps to Reproduce:
1. Register first user successfully
2. Attempt to register second user with same username
   
**Expected Result**: Username already exist error
**Actual Result**: Username already exist error
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: High
**Status**: Done

---

**Title**: Chatroom Creation
**Description**: Verify the creation of a new chatroom.

Steps to Reproduce:
1. Start server.
2. Connect client.
3. Select "Create Chatroom" option.
4. Enter a unique chatroom name.
   
**Expected Result**: Chatroom successfully created and added to the chatroom list.
**Actual Result**: Chatroom successfully created and added to the chatroom list.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: High.
**Status**: Done.

---

**Title**: Join Existing Chatroom
**Description**: Verify that a user can join an existing chatroom.

Steps to Reproduce:
1. Start server.
2. Create a chatroom.
3. Connect another client.
4. Select "Join Chatroom" and enter the name of the existing chatroom.

**Expected Result**: User successfully joins the existing chatroom.
**Actual Result**: User successfully joins the existing chatroom.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: High
**Status**: Done

---

**Title**: Message Broadcasting
**Description**: Verify that messages are delivered to all users in the chatroom.

Steps to Reproduce:
1. Start server.
2. Create a chatroom and join multiple users.
3. Send a message from one user.

**Expected Result**: All users in the chatroom receive the message.
**Actual Result**: All users in the chatroom receive the message.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: High.
**Status**: Done.

---

**Title**: Duplicate Chatroom
**Description**: Verify behavior when attempting to create a chatroom with an existing name.

Steps to Reproduce:
1. Start server
2. Create a chatroom
3. Attempt to create another chatroom with the same name

**Expected Result**: Error message indicating chatroom name already exists.
**Actual Result**: No error message, but doesn't create another chatroom
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: Medium
**Status**: Failed

---

**Title**: Leave Chatroom
**Description**: Verify behavior when a user leaves a chatroom.

Steps to Reproduce:
1. Start server
2. Join a chatroom
3. Select "Leave Chatroom" option

**Expected Result**: User successfully leaves the chatroom and no longer receives messages
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: High
**Status**: Done

---

**Title**: Admin Leave
**Description**: Verify behavior when the admin leaves the chatroom.

Steps to Reproduce:
1. Start server.
2. Create a chatroom (admin is creator).
3. Admin leaves the chatroom.

**Expected Result**: Admin role transfers to another user or chatroom is disbanded.
**Severity**: Medium
**Status**: Failed

---

**Title**: Simultaneous Messages
**Description**: Verify handling of concurrent message sending.

Steps to Reproduce:
1. Start server.
2. Join a chatroom with multiple users.
3. Simultaneously send messages from all users.

**Expected Result**: All messages are delivered without delay or corruption.
**Severity**: High.
**Status**: Done.

---

**Title**: Multiple Client Management
**Description**: Verify server handling of multiple clients.

Steps to Reproduce:
1. Start server.
2. Connect multiple clients.
3. Perform chatroom operations (create, join, leave) from each client.

**Expected Result**: Server maintains stable connections and processes client requests correctly.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: High.
**Status**: Done.

---

**Title**: Invalid Commands
**Description**: Verify server handling of invalid commands.

Steps to Reproduce:
1. Start server.
2. Connect client.
3. Enter an invalid command.

**Expected Result**: Error message indicating invalid command.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: High.
**Status**: Done.


---

**Title**: Menu Navigation
**Description**: Verify main menu navigation functionality.

**Steps to Reproduce**:
1. Start server.
2. Connect client.
3. Navigate through the main menu options.

**Expected Result**: User can successfully navigate all menu options.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: High.
**Status**: Done.



---

**Title**: Multiple Logins
**Description**: Verify behavior on multiple login attempts by the same user.

Steps to Reproduce:
1. Start server.
2. Connect client and log in.
3. Attempt to log in again with the same credentials.

**Expected Result**: Error message indicating the user is already logged in.
**Actual Result**: The user is able to login on two separate instances.
**Severity**: Medium.
**Status**: Failed

---

**Title**: Connection Limit
**Description**: Verify server behavior when the connection limit is reached.

Steps to Reproduce:
1. Start server.
2. Connect the maximum number of clients.
3. Attempt to connect additional clients.

**Expected Result**: Error message indicating the connection limit has been reached.
**Actual Result**: Error message indicating the connection limit has been reached.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: High.
**Status**: Not Done.

---

**Title**: Send Private Message
**Description**: Verify sending private messages to an online user.

**Steps to Reproduce**:
1. Start server.
2. Connect multiple clients.
3. Send a private message from one user to another.

**Expected Result**: Private message successfully delivered to the recipient.
**Environment**: Local dev environment (Python 3.11, SQLite).
**Severity**: Medium.
**Status**: Done.

---

**Title**: Message History
**Description**: Test viewing message history

**Steps to Reproduce**:
1. Start server
2. Connect client and log in
3. Access message history

**Expected Result**: Message history retrieved successfully
**Actual Result**: Message history retrieved successfully
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: Medium
**Status**: Done

---

**Title**: Read Status
**Description**: Test message read status tracking

**Steps to Reproduce**:
1. Start server
2. Connect client A and send a message to client B
3. Connect client B and read the message

**Expected Result**: Message marked as read
**Severity**: Medium
**Status**: Done

---

**Title**: Invalid Recipient
**Description**: Test sending to non-existent user

**Steps to Reproduce**:
1. Start server
2. Connect client and log in
3. Attempt to send a message to a non-existent user

**Expected Result**: Invalid recipient error 
**Actual Result**: Recipient not found error
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: Low
**Status**: Done

---

**Title**: Server Startup
**Description**: Test proper server initialization

**Steps to Reproduce**:
1. Start server
2. Verify logs for startup messages

**Expected Result**: Starts lister thread
**Expected Result**: Lister thread starts 
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: High
**Status**: Done

---

**Title**: Port Binding
**Description**: Test server port binding

**Steps to Reproduce**:
1. Start server
2. Check if the specified port is in use

**Expected Result**: Server binds to the port successfully
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: High
**Status**: Done

---

**Title**: Graceful Shutdown
**Description**: Test server shutdown process

**Steps to Reproduce**:
1. Start server
2. Initiate shutdown command

**Expected Result**: Server shuts down gracefully, releasing resources
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: Medium
**Status**: Done

---

**Title**: Client Cleanup
**Description**: Test cleanup after client disconnection

**Steps to Reproduce**:
1. Start server
2. Connect client and log in
3. Disconnect client

**Expected Result**: Client session cleaned up successfully
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: Medium
**Status**: Done

---

**Title**: Connection Load
**Description**: Test server under multiple connections

Steps to Reproduce:
1. Start server
2. Connect multiple clients simultaneously

**Expected Result**: Server handles connections without issues
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: High
**Status**: Done

---

**Title**: Password Encryption
**Description**: Verify password hashing

Steps to Reproduce:
1. Start server
2. Register a new user with a password
3. Check database for stored password

**Expected Result**: Password stored as a hash
**Actual Result**: Passwords are stored as a hash
**Environment**: Local dev environment (Python 3.11, SQLite)
**Severity**: High
**Status**: Done


---
### Bug Reports
```
Title: [Active Clients # in Server not updating when user signs out]
Description: [Detailed description]
Steps to Reproduce:
1. [Step 1]
2. [Step 2]
...
Expected Result: [What should happen]
Actual Result: [What actually happens]
Environment: [Test environment details]
Severity: [High/Medium/Low]
Status: [Open/In Progress/Fixed]
```

```
Title: [Error message shows but succesfully removes user account]
Description: [Detailed description]
Steps to Reproduce:
1. [Step 1]
2. [Step 2]
...
Expected Result: [What should happen]
Actual Result: [What actually happens]
Environment: [Test environment details]
Severity: [High/Medium/Low]
Status: [Open/In Progress/Fixed]
```


```
Title: [ /view Error]
Description: When a user executes the /view command to see chatroom users, the client interface becomes unresponsive to new input. Users cannot type new commands or messages after viewing the user list.
Steps to Reproduce:
1. Connect to server and join a chatroom
2. Execute /view command to see chatroom users
3. Attempt to type new commands or messages
Expected Result: User should be able to continue typing and sending messages after viewing chatroom users
Actual Result: Client becomes unresponsive to keyboard input, requiring restart of client application
Environment: Python 3.11, SQLite 3.39.5, Local test environment
Severity: High
Status: Open
```







