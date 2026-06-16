#!/bin/sh

###
### Script to run grafana and the data source
###

# remove old stuff
set +e # keep running if there are errors
podman stop grafana data_source || echo "no containers to stop"
podman rm grafana data_source || echo "no containers to remove"
podman network rm monitoring_network || echo "no network to remove"
set -e # stop running if there are errors

# Remove any previous volumes
podman volume rm $(podman volume ls -qf dangling=true)

# remove the old containers, if any
podman compose down # default is --file docker-compose.yml

# build and run the containers
podman compose up -d # default is --file docker-compose.yml

sleep 2
# see what is running
podman ps -a
