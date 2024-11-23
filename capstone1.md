# TCP chat app

- The project to be an executable file so the user can open the app easily. Once the file is opened , the command line will prompt the user for their user name and password. If the user doesn't 
have an account, they can type a command to make an account.
    - The user will be prompted to make a username and password for the app

- Once the user has succesfully entered the chat app, the user will be greeted with a main menu. On that menu the user will be prompted with 3 options, to __create__ a chat room, __join__ a chat room and to __compose__ of a message (private message)

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
    - When a user either joins or creates a chat, They will be able to send and recive messages they will see a list of connected clients and also they will be prompted a list of commands that can help the user use the app. (User Experience commands)
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



        

User authentication and admin functionality.
Inclusion and functionality of chat rooms.
Messaging behavior, encryption, and storage.