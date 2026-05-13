###
### PowerShell Script to connect into the local postgres container
###

Write-Output "Connecting to local postgres container..."

docker exec -it my-postgres su postgres

# after that starts and shows you a terminal, use the "psql" command
