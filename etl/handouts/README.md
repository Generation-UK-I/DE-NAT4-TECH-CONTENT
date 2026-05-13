# ETL SoT handouts

PostgreSQL Docker and Podman files are provided for running your database.

## Setup

We now need to run two containers, one for PostgresSQL and one for Adminer (a DB Admin UI).

### Podman setup (default)

> Only do this _or_ the Docker setup, you do not need both

1. Open a terminal in the `handouts` folder
1. Check Podman is running with `podman machine list`
1. If the machine is not started, then turn it on by running `podman machine start`
1. Run `podman ps -a` to check for old containers
    1. Stop all of them by running `podman stop <container_name>`
    1. Remove all of them by running `podman rm <container_name>`
1. If you have `podman compose` installed and working,
    1. Run one of these:
        - `./podman-compose-run.sh` (MacOS / Unix / GitBash), or
        - `./podman-compose-run.ps1` (Powershell)
1. Else if you do not have `podman compose` installed and working,
    1. run one of these:
        - `./podman-run.sh` (MacOS / Unix / GitBash)
        - `./podman-run.ps1` (Powershell)

### Docker setup (if not using Podman)

> Only do this _or_ the Podman setup, you do not need both

1. Open a terminal in the `handouts` folder
1. Run `docker ps -a` to check for old containers
    1. Stop all of them by running `docker stop <container_name>`
    1. Remove all of them by running `docker rm <container_name>`
1. If you have `docker compose` installed and working,
    1. Run one of these:
        - `./docker-compose-run.sh` (MacOS / Unix / GitBash), or
        - `./docker-compose-run.ps1` (Powershell)
1. Else if you do not have `docker compose` installed and working,
    1. Run one of these:
    - `./docker-run.sh` (MacOS / Unix / GitBash)
    - `./docker-run.ps1` (Powershell)

## Getting a terminal in the running PostgreSQL container

After one of the above scripts is run, you can open a terminal inside the running PostgreSQL server, and use the `psql` tool to execute SQL directly on the database.

If using Podman (default), run

- either `./exec-into-postgres-podman.sh`(MacOS / Unix / GitBash), or
- or `./exec-into-postgres-podman.ps1` (Powershell)
- then
    - after either of the above, run `psql` in the container

If using Docker, run

- either `./exec-into-postgres-docker.sh`(MacOS / Unix / GitBash), or
- or `./exec-into-postgres-docker.ps1` (Powershell)
- then
    - after either of the above, run `psql` in the container

## Using a venv

> You can either re-use an existing venv, or create a new one just for this session. To use an existing one, jump ahead to the `Activate` step below.

1. You can create a virtual environment with python by running:
    - `python3 -m venv .venv` (MacOS / Unix / GitBash)
    - `python3 -m venv .venv` (Powershell - same as above until venv is activated)
1. Activate your virtual environment by running:
    - `source .venv/bin/activate` (MacOS / Unix / GitBash)
    - `.venv\Scripts\activate.ps1` (Powershell)
1. Install the `requirements.txt` file by running:
    - `python3 -m pip install -r requirements.txt` (MacOS / Unix / GitBash)
    - `python -m pip install -r requirements.txt` (Powershell)
