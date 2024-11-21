'''
testChat_concurrent.sh 

  @author Osagie Owie
  @email owieo204@potsdam.edu
  @course CIS 480 Senior Project
  @assignment: Senior Project
  @due 12/9/24 
 '''
#!/bin/bash

echo Start the server in the background
python3 server.py --host 127.0.0.1 --port 9090 &
SERVER_PID=$!
echo "Server started with PID $SERVER_PID"
sleep 2

# Start multiple clients in the background and send messages simultaneously
echo "Starting Client 1 (Alice)..."
(
  echo "Alice"   # Name for Client 1
  echo "Hi from Alice!"
  echo "How's everyone?"
  echo "/quit"    # Alice disconnects
) | python3 client.py --host 127.0.0.1 --port 9090 &
CLIENT1_PID=$!
echo "Client 1 (Alice) started with PID $CLIENT1_PID"
echo "Starting Client 2 (Bob)..."
(
  echo "Bob"      # Name for Client 2
  echo "Hey Alice!"
  echo "I'm good, how about you?"
  echo "/quit"    # Bob disconnects
) | python3 client.py --host 127.0.0.1 --port 9090 &
CLIENT2_PID=$!
echo "Client 2 (Bob) started with PID $CLIENT2_PID"
echo "Starting Client 3 (Charlie)..."
(
  echo "Charlie"  # Name for Client 3
  echo "Hi everyone!"
  echo "What's up?"
  echo "/quit"    # Charlie disconnects
) | python3 client.py --host 127.0.0.1 --port 9090 &
CLIENT3_PID=$!
echo "Client 3 (Charlie) started with PID $CLIENT3_PID"

# Wait for a few seconds to let clients exchange messages
sleep 15

# Clean up: Kill the server and clients
# kill $SERVER_PID $CLIENT1_PID $CLIENT2_PID $CLIENT3_PID
# echo "Processes terminated."
