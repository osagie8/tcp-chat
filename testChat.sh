'''
testChat.sh 

  @author Osagie Owie
  @email owieo204@potsdam.edu
  @course CIS 480 Senior Project
  @assignment: Senior Project
  @due 12/9/24 
 '''
#!/bin/bash

# Start the server in the background
python3 server.py --host 127.0.0.1 --port 9090 &
SERVER_PID=$!
echo "Server started with PID $SERVER_PID"
sleep 2

# Start multiple clients in the background and provide names
(
  echo "Alice"   # Name for Client 1
  sleep 1
  echo "Hi, I'm Alice!"
  sleep 2
  echo "/quit"    # Alice disconnects
) | python3 client.py --host 127.0.0.1 --port 9090 &
CLIENT1_PID=$!
echo "Client 1 (Alice) started with PID $CLIENT1_PID"
sleep 1

(
  echo "Bob"      # Name for Client 2
  sleep 1
  echo "Hello, Alice!"
  sleep 2
  echo "Bye!"
  sleep 1
  echo "/quit"    # Bob disconnects
) | python3 client.py --host 127.0.0.1 --port 9090 &
CLIENT2_PID=$!
echo "Client 2 (Bob) started with PID $CLIENT2_PID"
sleep 1

# Wait for a few seconds to let clients exchange messages
sleep 5

# Clean up: Kill the server and clients
#kill $SERVER_PID $CLIENT1_PID $CLIENT2_PID
#echo "Processes terminated."

