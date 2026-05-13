# See https://stackoverflow.com/a/65570275/23819566, "GitBash: How to stop MinGW and MSYS from mangling path names given at the command line"
$env:MSYS2_ARG_CONV_EXCL = "*" # Stops MinGW and MSYS from fiddling with paths
$env:MSYS_NO_PATHCONV = 1      # Stops GitBash fiddling with paths

###
### Script to create local postgres and adminer containers
###

Write-Output ""
Write-Output "Starting local postgres and adminer containers..."

# remove old stuff
Write-Output "removing old containers..."
$ErrorActionPreference = "Continue" # PS equivalent of set +e in bash
podman stop my-postgres my-adminer; if (-not $?) { Write-Output "no containers to stop" };
podman rm my-postgres my-adminer; if (-not $?) { Write-Output "no containers to remove" };
podman network rm databases_network; if (-not $?) { Write-Output "no network to remove" };
# PowerShell equivalent of set -e command in bash. Exits script if error occurs in following commands
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
podman compose up --build -d # default is --file docker-compose.yml

# Check it is running
Write-Output ""
podman ps -a;
Write-Output ""

# Check what happened in the sql scripts
Write-Output ""
podman logs my-postgres;
Write-Output ""

Write-Output "all done"
