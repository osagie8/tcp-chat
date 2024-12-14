
## Backlog Items Completed

## User Stories
**Main Menu**
- As a user of the chat app, I want to see a main menu after logging in so that I can easily navigate the app’s features.
- As a user of the chat app, I want to create a new chatroom from the main menu so that I can start a group conversation.
- As a user of the chat app, I want to join an existing chatroom from the main menu so that I can participate in group conversations.
- As a user of the chat app, I want to compose a private message from the main menu so that I can communicate directly with another user.
- As a user of the chat app, I want to type a command to view my private messages so that I can access my private chats quickly.

**Registration and login**
- As a user of the chat app, I want to register a unique username and password so that I can securely access the app.
- As a user of the chat app, I want the system to enforce password standards (Symbol and number required) so that I can ensure my account's security.
- As a user of the chat app, I want to log in with my username and password so that I can access my account and chats.
- As a user of the chat app, I want to be notified if my username is already taken so that I can choose a another unique username.


**User Management**
- As a user of the chat app, I want to see a list of all online users so that I can know who is available to chat.
- As a user of the chat app, I want to register a username when connecting to the server so that I can be identified uniquely in the chat.
- As a user of the chat app, I want to log out of the application so that I can disconnect securely.
- As a user of the chat app, I want to be notified when another user logs in or logs out so that I can track user activity.

**Group Chat**
- As a user of the chat app, I want to create a group chat with a custom name so that I can organize discussions with specific users.
- As a user of the chat app, I want to invite other users to a group chat so that I can collaborate.
- As a user of the chat app, I want to be notified when I am added to a group chat so that I can decide whether to participate.
- As a user of the chat app, I want to leave a group chat so that I can exit discussions that are no longer relevant.

**Private Messaging**
- As a user of the chat app, I want to send a direct message to another user by name so that I can communicate privately.
- As a user of the chat app, I want to see a separate notification for private messages so that I can differentiate private from public communications.
- As a user of the chat app, I want to view a list of my private conversations so that I can revisit past messages.
- As a user of the chat app, I want to delete specific private messages so that I can remove sensitive or irrelevant content.

**App Error Behavior**
- As a user of the chat app, I want to receive an error message if my connection to the server is lost so that I can troubleshoot the issue.
- As a user of the chat app, I want to reconnect to the server automatically so that I can resume chatting without manual intervention.
- As a user of the chat app, I want to know when the server is shutting down so that I can prepare for disconnection.

**Security**
- As a user of the chat app, I want all my messages to be encrypted so that I can ensure the security of my communications.
- As a user of the chat app, I want the system to check my credentials before login so that I can prevent unauthorized access to my account.

**Database**
- As the developer, I want to store user information (username/password) in a database so that I can track user accounts securely.
- As the developer, I want to store messages in the database so that I can preserve chat histories for users.

**Testing**
- As the developer, I want to test server start-up and listening capabilities so that I can ensure the app is running correctly.
- As the developer, I want to test client connections so that I can ensure reliable communication between clients and the server.
- As the developer, I want to simulate multiple client connections so that I can ensure the app can handle concurrent users.
- As the developer, I want to test database queries so that I can verify data and retrieval accuracy.
- As the developer, I want to test message encryption and decryption so that I can ensure secure communication.


## Tasks

**Main Menu**
- Design and implement the main menu UI.
- Implement the option to create a new chatroom.
- Implement the option to join an existing chatroom by entering a chatroom ID.
- Implement the option to compose a private message from the main menu.
- Implement a command to view private messages directly from the main menu.
**Registration and Login**
- Implement user registration, which includes checking for unique usernames and enforcing password standards.
- Implement user login functionality.
- Validate credentials during login.
- Display an error message if the username is already taken during registration.
**User Management**
- Implement user registration with a unique username.
- Develop functionality to display a list of all online users.
- Implement a feature to allow users to change their username dynamically while connected.
- Implement a logout feature to disconnect users securely.
- Notify users when someone logs in or out.
**Group Chat**
- Implement functionality to create a group chat with a custom name.
- Allow admins to invite users to a group chat.
- Implement notifications for users when they are added to a group chat.
- Enable users to leave a group chat and handle cleanup tasks (e.g., removing them from the list of participants).
- Ensure that when the admin leaves, the group chat is closed.
**Private Messaging**
- Implement functionality to send a direct message to another user by their username.
- Develop notifications for private messages, distinguishing them from public messages.
- Implement a feature to view a list of private conversations.
- Implement functionality to delete private messages from a user’s inbox.
**App Behavior**
- Implement error handling for server disconnections with user-facing error messages.
- Develop an automatic reconnection mechanism for users.
- Notify users when the server is shutting down.
- Security
- Integrate PyCryptodome to encrypt all messages sent between users.
- Validate user credentials securely before allowing login.
- Implement measures to ensure secure password storage (e.g., hashing).
**Database**
- Create a database schema for storing user information, including username and hashed password.
- Create a database schema for storing chat messages, including sender ID and content.
- Create a database schema for storing chatroom details, including room ID and admin ID.
**Testing**
- Write test cases for server startup and listening capabilities.
- Write test cases to handle invalid port errors.
- Write test cases for successful client connections.
- Write test cases for database operations (e.g., adding, retrieving, and deleting users/messages).
- Simulate and test multiple concurrent client connections.
- Write test cases for message encryption and decryption.
- Test server reconnection behavior for clients.
- Simulate and test real-world scenarios using virtual machines and networks.
 

## Product Backlog

**Main Menu**
1. __[1 Priority]__ Design and implement the main menu UI.
__Acceptance requirements:__ Users can navigate the app’s features using the command-line interface.
2. __[1 Priority]__ Implement the option to create a new chatroom.
__Acceptance requirements:__  Users can select "Create Chatroom" and proceed to configure a chatroom.
3. __[1 Priority]__  Implement the option to join an existing chatroom by entering a chatroom ID.
__Acceptance requirements:__  Users can enter a valid chatroom ID and join the room.
4. __[2 Priority]__  Implement the option to compose a private message from the main menu.
__Acceptance requirements:__  Users can select "Compose Message" to send a private message.
5. __[2 Priority]__  Implement a command to view private messages directly from the main menu.
__Acceptance requirements:__  Users can type a specific command to access their private chat inbox.

**Registration and Login**
1. __[1 Priority]__ Implement user registration
__Acceptance requirements:__ Users can register securely, and the system validates uniqueness and password complexity.
2. __[1 Priority]__ Implement user login functionality.
__Acceptance requirements:__ Users can log in using their registered username and password.
3. __[1 Priority]__ Validate credentials during login.
__Acceptance requirements:__ Login succeeds only if credentials are correct.
4. __[2 Priority]__ Display an error message if the username is already taken during registration.
__Acceptance requirements:__ Users receive a clear error message for duplicate usernames.

**User Management**
1. __[1 Priority]__ Implement user registration with a unique username.
__Acceptance requirements:__ Users can create unique usernames at registration.
2. __[2 Priority]__ Develop functionality to display a list of all online users(UserID).
__Acceptance requirements:__ Users can see a list of active users in the system.
3. __[2 Priority]__ Implement a feature to allow users to change their username dynamically while connected.
__Acceptance requirements:__ Users can update their usernames during a session.
4. __[1 Priority]__ Implement a logout feature to disconnect users securely.
__Acceptance requirements:__ Users can log out and are removed from the active user list.
5. __[2 Priority]__ Notify users when someone logs in or out.
__Acceptance requirements:__ Users receive notifications of login/logout events.

**Group Chat**
1. __[1 Priority]__ Implement functionality to create a group chat with a custom name.
__Acceptance requirements:__ Users can name and create a new group chat.
2. __[2 Priority]__ Allow admins to invite users to a group chat.
__Acceptance requirements:__  Admins can add participants by username.
3. __[2 Priority]__ Implement notifications for users when they are added to a group chat.
__Acceptance requirements:__  Users receive notifications of being added to groups.
3. __[2 Priority]__  Enable users to leave a group chat and handle cleanup tasks.
__Acceptance requirements:__  Users can exit groups, and the group updates accordingly.
4. __[1 Priority]__  Ensure that when the admin leaves, the group chat is closed.
__Acceptance requirements:__  The system disbands groups if the admin exits.

**Private Messaging**
1. __[1 Priority]__  Implement functionality to send a direct message to another user by their username.
__Acceptance requirements:__  Users can send private messages to specific users.
2. __[2 Priority]__  Develop notifications for private messages, distinguishing them from public messages.
__Acceptance requirements:__  Users receive notifications for private messages.
3. __[2 Priority]__  Implement a feature to view a list of private conversations.
__Acceptance requirements:__  Users can access and scroll through private message threads.
4. __[2 Priority]__  Implement functionality to delete private messages from a user’s inbox.
__Acceptance requirements:__  Users can remove private messages from their view.

**App Error Behavior**
1. __[1 Priority]__  Implement error handling for server disconnections with user-facing error messages.
__Acceptance requirements:__  Users are notified when their connection is lost.
2. __[2 Priority]__  Develop an automatic reconnection mechanism for users.
__Acceptance requirements:__  Users automatically reconnect without losing session state.
3. __[2 Priority]__  Notify users when the server is shutting down.
__Acceptance requirements:__  Users receive a warning when the server is about to stop.

**Security**
1. __[1 Priority]__  Integrate PyCryptodome to encrypt all messages sent between users.
__Acceptance requirements:__ All messages are securely encrypted before transmission.
2. __[1 Priority]__  Validate user credentials securely before allowing login.
__Acceptance requirements:__  Credentials are verified without exposing sensitive data.
3. __[2 Priority]__  Implement measures to ensure secure password storage (e.g., hashing).
__Acceptance requirements:__  Passwords are hashed using industry standards.

**Database**
1. __[1 Priority]__ Create a database schema for storing user information, including username and hashed password.
__Acceptance requirements:__  User data is securely stored in the database.
2. __[1 Priority]__ Practice SQLite Create, Read, Update, Delete operations.
__Acceptance requirements:__  General understanding of the operations(Testing)
3. __[1 Priority]__  Create a database schema for storing chat messages, including sender ID and content.
__Acceptance requirements:__  Messages are stored and retrievable by user and chatroom.
4. __[2 Priority]__  Create a database schema for storing chatroom details, including room ID and admin ID.
__Acceptance requirements:__  Chatroom details are persisted for session management.


**Testing**
1. __[1 Priority]__  Write test cases for server startup and listening capabilities.
__Acceptance requirements:__  Tests ensure the server starts and listens on valid ports.
2. __[1 Priority]__  Write test cases to handle invalid port errors.
__Acceptance requirements:__  The system gracefully handles invalid port scenarios.
3. __[2 Priority]__  Write test cases for successful client connections.
__Acceptance requirements:__  Tests confirm multiple clients can connect successfully.
4. __[2 Priority]__  Write test cases for database operations (e.g., adding, retrieving, and deleting users/messages).
__Acceptance requirements:__  Database interactions function correctly and securely.
5. __[2 Priority]__  Simulate and test multiple concurrent client connections.
__Acceptance requirements:__  The app maintains stability under high concurrency.
6. __[2 Priority]__  Write test cases for message encryption and decryption.
__Acceptance requirements:__  Encrypted messages are transmitted and decrypted correctly.
7. __[2 Priority]__  Test server reconnection behavior for clients.
__Acceptance requirements:__  Clients reconnect seamlessly after disconnection.
8. __[3 Priority]__  Simulate and test real-world scenarios using virtual machines and networks.
__Acceptance requirements:__ The system works as expected in real-world environments.



