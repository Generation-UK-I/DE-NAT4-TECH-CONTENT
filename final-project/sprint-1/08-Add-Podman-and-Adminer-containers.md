# DE-NAT4

>You can re-use your Adminer/Postgres Docker environment, but you may still need to figure out how to automate it

## Add Podman and Adminer containers

## Description

In order to make swift movements on the PoC, we need to establish a docker-compose file which will be stored in our project repository so that every member has the correct containers setup.

As the data warehouse we plan on using is based on [PostgreSQL](https://hub.docker.com/_/postgres), we will need to spin up a container for it.

We should also make use of a container that can run [Adminer](https://hub.docker.com/_/adminer) for us too so we can query the data easily.

You will need to set up one or both of:

- For use in GitBash, a bash script (`*.sh`)
- For use in PowerShell, a powershell script (`*.ps1`)

### Suggestions

Adding DB support to your project - you can do something like this (copying files from the "databases-sot" or "etl-sot" sessions)

- make a `databases` folder
  - into it add
  - `docker-compose.yml`
  - `replace_cniVersion.py`
  - `setup-all-podman.sh`
  - a sub-folder called `db-scripts` with your schema sql files - these will run on boot of the container
- in your `src` or other code folder
  - add `requirements.txt`
- in your main `README.md`
  - add instructions for activating a `venv` and adding the requirements
  - add instructions for starting up the containers
    - e.g. with
      - `podman compose down`
      - `podman compose up -d`
    - and/or with
      - `./setup-podman.all.sh`

## User Story

**As a** developer
**I want** to create a docker-compose.yml file
**So that** I can share the same infrastructure with my team

## Acceptance Criteria

- [ ] todo
- [ ] todo
- [ ] todo
