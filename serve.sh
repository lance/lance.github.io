#!/bin/bash

# Make sure we don't have a server currently running
if [ -e server.pid ] ; then
  kill `cat server.pid`
fi

# Run the server
/usr/bin/env node build serve 2>&1 &

# Write the PID to a file
echo $! > server.pid

# Sleep for a few seconds to let the server do it's thing
sleep 3

# open site in a browser
open http://localhost:8080

# tail the logs
tail -f server.log
