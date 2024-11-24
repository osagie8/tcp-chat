# TCP chat app

- The project to be an executable file using pyInstaller so the user can open the app easily. Once the file is opened , the command line will prompt the user for their user name and password. If the user doesn't 
have an account, they can type a command to make an account.
    - The user will be prompted to make a username and password for the app
        - The system will not allow duplicates
        - Does the app will have its own password standards for added security
        
- Main menu:

    1. Create a chat room
    2. Join a chat room
    3. Compose a private message
    4. View private chats


- Once the user has succesfully entered the chat app, the user will be greeted with a main menu. On that menu the user will be prompted with 3 options, to __create__ a chat room, __join__ a chat room and to __compose__ of a message (private message).
    - The user can type -in to view inbox while in the main menu.

### Create a chat room
    - The creater of the room is __Admin__ of the group by default. 
        - The admin is asked to set the name of the chat room and how many people are allowed in.
            - Admin create groups and are allowed to kick clients from group as well.
        - The group ID , will be shown on the top so it can be easy to share.
    - eg. *User selects create chat room*
        - Admin enters a unique name for the chat room.
        - Admin specifies the maximum number of participants.
        - System generates and displays the group ID with the admin being the only client.

### Join a chat room
    - Upon opening the application, a user that intends to join a chat room will be told the chat room ID. Whcih they can enter to join a specific chat room.
### Chat room exerience
    - When a user either joins or creates a chat, They will be able to send and recive messages they will see a list of connected clients and also they will be prompted a list of commands that can help the user use the app. (User Experience commands). Clients that arent in the chat room can't see the messages happening in the chat room.
        - eg. *User joins chat*
            - Welcome to Osagie's chatroom (#2421)
                - Connected clients
                    - Osagie (Admin)
                    - Bob
                    - Joe
                    - Sally
                    - Brian 
            - Press /q to leave chat
            - Press /l to list connected users
            - To close the group the admin must leave.
        - When a client leaves for any reason, it will be broadcasted to the other remaining clients.
        - Once the admin of the group leaves the chat the chat room will close and all of the clients will go back to the __main menu__.
        - User Messages will be stored in the database for the grouchat.

### Private Chats

- While in the main menu the user can start a private chat with another user directly by username by selecting compose a message.
- While in the main menu the user can type in " -in "  to view private chat dialouge with other users.

### Database Design

I plan to use SQLite and the schema for this app will have 3 tables where I will be storing data in which is the
- Users table
- Messages table
- Chat Room table

## Users table

The user table will used to store the ID for easy refrence, the username of clients and their passwords.

| Column Name    | Data Type       | Constraints                                  |
|----------------|-----------------|----------------------------------------------|
| userId         | INT             | PRIMARY KEY, UNIQUE, AUTO_INCREMENT, NOT NULL|
| userName       | VARCHAR(50)     | UNIQUE, NOT NULL                             |
| password       | VARCHAR(255)    | NOT NULL 

- The user ID will be INT and will be used as the primary key because It would be the most ideal to target a unique number to identify a client. The user Id will need to be diffrent for each user,
so the userID will update with every added entry with the auto increment contraint
- The userName will be a able to store up to 50 characters. This value will be have to be a unique value so everyone's name can be different.
- The password table will be a able to store up to 255 characters. This doesn't have to be unique but every user must make a password.

## Messages

The message table will be used to only store what was said and who sent it.

| Column Name    | Data Type       | Constraints                                  |
|----------------|-----------------|----------------------------------------------|
| messageId      | INT             | PRIMARY KEY, UNIQUE, AUTO_INCREMENT, NOT NULL|
| message        | TEXT            | NOT NULL                                     |
| userID         | INT             | FOREIGN KEY on userID 

- The message ID will be INT and will be used as the primary key for easy refrence.
- The message column will store the content of messages
- The UserID will be an INT and is the same colmun as the userID in the users table. These tables
are tied together so each message will can also be tied to its user.

## Chat Rooms

The chat room table will be used to store the roomID for easy refrence the room Name who created the group.
All messages sent in the chat rooms can be seen from the messages table.

| Column Name    | Data Type       | Constraints                                  |
|----------------|-----------------|----------------------------------------------|
| roomId         | INT             | PRIMARY KEY, UNIQUE, AUTO_INCREMENT, NOT NULL|
| roomName       | VARCHAR(50)     | UNIQUE, NOT NULL                             |

- The roomID will be INT and will be used as the primary key for easy refrence.
- The roomName will be INT and will be used as the primary key for easy refrence.

A link to a user experience __[flow chart](https://ibb.co/HHvK6N1)__ is below.

__https://ibb.co/HHvK6N1__

