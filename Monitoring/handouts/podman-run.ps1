###
### Script to create local grafana and data_source containers
###

# remove old stuff
$ErrorActionPreference = "Continue" # keep running if there are errors
podman stop grafana data_source; if (-not $?) { Write-Output "no containers to stop" }
podman rm grafana data_source; if (-not $?) { Write-Output "no containers to remove" }
podman network rm monitoring_network; if (-not $?) { Write-Output "no network to remove" }
# PS equivalent of set -e command on bash. Exits script when an error occurs.
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

# Remove any previous volumes
$volumes = podman volume ls -qf "dangling=true"
if ($volumes) {
    podman volume rm $volumes
}

# Create bridge network
podman network create monitoring_network

python3 replace_cniVersion.py ~/.config/cni/net.d/databases_network.conflist

# Run grafana container with network alias name "grafana"
podman run -d `
  --name grafana `
  --network monitoring_network `
  -p 3000:3000 `
  -v grafana:/var/lib/grafana `
  docker.io/grafana/grafana:latest

# build data source image containing python code
podman build -t data_source_image .

# Run flask data source container with network alias name "data_source"
podman run -d `
  --name data_source `
  --network monitoring_network `
  -p 5000:5000 `
  -v ./app.py:/app/app.py `
  data_source_image

Start-Sleep -Seconds 2
# see what is running
podman ps -a
