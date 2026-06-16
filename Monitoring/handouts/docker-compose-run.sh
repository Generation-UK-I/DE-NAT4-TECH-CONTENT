#!/bin/sh

###
### Script to run grafana and the data source
###

# remove old stuff
set +e # keep running if there are errors
docker stop grafana data_source || echo "no containers to stop"
docker rm grafana data_source || echo "no containers to remove"
docker network rm monitoring_network || echo "no network to remove"
set -e # stop running if there are errors

# Remove any previous volumes
docker volume rm $(docker volume ls -qf dangling=true)

# remove the old containers, if any
docker compose down # default is --file docker-compose.yml

# build and run the containers
docker compose up -d # default is --file docker-compose.yml

sleep 2
# see what is running
docker ps -a
