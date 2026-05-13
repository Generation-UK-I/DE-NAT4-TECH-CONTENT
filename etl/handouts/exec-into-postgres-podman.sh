#!/bin/sh

###
### Script to connect into the local postgres container
###

echo "Connecting to local postgres container..."

podman exec -it my-postgres su postgres

# after that starts and shows you a terminal, use the "psql" command
