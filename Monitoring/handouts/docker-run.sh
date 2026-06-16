#!/bin/sh

# remove old stuff
set +e # keep running if there are errors
docker stop grafana data_source || echo "no containers to stop"
docker rm grafana data_source || echo "no containers to remove"
docker network rm monitoring_network || echo "no network to remove"
set -e

# Remove any previous volumes
docker volume rm $(docker volume ls -qf dangling=true)

# Create bridge network
docker network create monitoring_network

# Run grafana container with network alias name "grafana"
docker run -d \
  --name grafana \
  --network monitoring_network \
  -p 3000:3000 \
  -v grafana:/var/lib/grafana \
  docker.io/grafana/grafana:latest

# build data source image containing python code
docker build -t data_source_image .

# Run flask data source container with network alias name "data_source"
docker run -d \
  --name data_source \
  --network monitoring_network \
  -p 5000:5000 \
  -v ./app.py:/app/app.py \
  data_source_image

sleep 2
# see what is running
docker ps -a
