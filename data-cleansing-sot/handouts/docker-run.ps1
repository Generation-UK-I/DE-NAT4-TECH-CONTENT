###
### Script to create local postgres and adminer containers
###

Write-Output ""
Write-Output "Starting local postgres and adminer containers..."

# remove old stuff
Write-Output "...removing old containers..."
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

docker network create databases_network

$SRC = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "db-scripts"

# Start it
# The scripts in ./db-scripts are executed in lexicographical order
docker run --name my-postgres `
  --network databases_network `
  -p 5432:5432 `
  -v "$SRC`:/docker-entrypoint-initdb.d" `
  -e POSTGRES_PASSWORD=mysecretpassword `
  -d docker.io/postgres;

Write-Output ""
Write-Output "...starting adminer container..."
docker run --name my-adminer `
  --network databases_network `
  -p 8080:8080 `
  -d docker.io/adminer;

# Check it is running
Write-Output ""
docker ps -a;
Write-Output ""

# Check what happened in the sql scripts
Write-Output ""
docker logs my-postgres;
Write-Output ""

Write-Output "all done"
