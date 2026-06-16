###
### Script to run grafana and the data source
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

# remove the old containers, if any
podman compose down # default is --file docker-compose.yml

# build and run the containers
podman compose up -d # default is --file docker-compose.yml

Start-Sleep -Seconds 2
# see what is running
podman ps -a
