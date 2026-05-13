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

# remove the old containers, if any
podman compose down # default is --file docker-compose.yml

# build and run the containers
podman compose up --build -d # default is --file docker-compose.yml

# Check it is running
echo ""
podman ps -a;
echo ""

# Check what happened in the sql scripts
echo ""
podman logs my-postgres;
echo ""

echo "all done"
