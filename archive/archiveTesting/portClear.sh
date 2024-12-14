#!/bin/bash

# Check if a port number is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <port>"
  exit 1
fi

PORT=$1

# Check if the port is in use
echo "Checking if port $PORT is in use..."
PID=$(lsof -t -i:$PORT)

if [ -n "$PID" ]; then
  echo "Port $PORT is in use by process $PID. Killing the process..."
  kill -9 $PID
  echo "Process $PID killed. Port $PORT is now free."
else
  echo "Port $PORT is not in use."
fi