#!/bin/sh

# See https://stackoverflow.com/a/65570275/23819566, "GitBash: How to stop MinGW and MSYS from mangling path names given at the command line"
export MSYS2_ARG_CONV_EXCL="*" # Stops MinGW and MSYS from fiddling with paths
export MSYS_NO_PATHCONV=1      # Stops GitBash fiddling with paths

###
### Script to create local postgres and adminer containers
###

echo ""
echo "Starting local postgres and adminer containers..."

# remove old stuff
echo "...removing old containers..."
set +e; # continue if there are errors
podman stop my-postgres my-adminer || echo "no containers to stop";
podman rm my-postgres my-adminer || echo "no containers to remove";
podman network rm databases_network || echo "no network to remove";
set -e; # stop if there are errors

# Remove any previous volumes
podman volume rm $(podman volume ls -qf dangling=true)

# Create bridge network
podman network create databases_network

python3 replace_cniVersion.py ~/.config/cni/net.d/databases_network.conflist

# The double quotes here are designed to work in GitBash
SRC="$(cd "$(dirname "$0")"; "pwd")/db-scripts"

# The scripts in ./db-scripts are executed in lexographical order
# Start it
podman run --name my-postgres \
  --network databases_network \
  -p 5432:5432 \
  -v "${SRC}":/docker-entrypoint-initdb.d \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -d docker.io/postgres;

podman run --name my-adminer \
  --network databases_network \
  -p 8080:8080 \
  -d docker.io/adminer;

# Check it is running
echo ""
podman ps -a;
echo ""

# Check what happened in the sql scripts
echo ""
podman logs my-postgres;
echo ""

echo "all done"
