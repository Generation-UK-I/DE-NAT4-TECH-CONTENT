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
docker stop my-postgres my-adminer || echo "no containers to stop";
docker rm my-postgres my-adminer || echo "no containers to remove";
docker network rm databases_network || echo "no network to remove";
set -e; # stop if there are errors

# Remove any previous volumes
docker volume rm $(docker volume ls -qf dangling=true)

docker network create databases_network

# The double quotes here are designed to work in GitBash
SRC="$(cd "$(dirname "$0")"; "pwd")/db-scripts"

# Start it
# The scripts in ./db-scripts are executed in lexicographical order
docker run --name my-postgres \
  --network databases_network \
  -p 5432:5432 \
  -v "${SRC}":/docker-entrypoint-initdb.d \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -d docker.io/postgres;

echo ""
echo "...starting adminer container..."
docker run --name my-adminer \
  --network databases_network \
  -p 8080:8080 \
  -d docker.io/adminer;

# Check it is running
echo ""
docker ps -a;
echo ""

# Check what happened in the sql scripts
echo ""
docker logs my-postgres;
echo ""

echo "all done"
