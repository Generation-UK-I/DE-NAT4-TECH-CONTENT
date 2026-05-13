###
### Script to create local postgres and adminer containers
###

# remove old stuff
Write-Output "removing old containers..."
$ErrorActionPreference = "Continue" # PS equivalent of set +e in bash
docker stop my-postgres my-adminer; if (-not $?) { Write-Output "no containers to stop" };
docker rm my-postgres my-adminer; if (-not $?) { Write-Output "no containers to remove" };
docker network rm databases_network; if (-not $?) { Write-Output "no network to remove" };
# PowerShell equivalent of set -e command in bash. Exits script if error occurs in following commands
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

# Remove any previous volumes
$volumes = docker volume ls -qf "dangling=true"
if ($volumes) {
    docker volume rm $volumes
}

# remove the old containers, if any
docker-compose down # default is --file docker-compose.yml

# build and run the containers
docker-compose up --build -d # default is --file docker-compose.yml

# Check it is running
Write-Output ""
docker ps -a;
Write-Output ""

# Check what happened in the sql scripts
Write-Output ""
docker logs my-postgres;
Write-Output ""

Write-Output "all done"
