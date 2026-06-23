#!/bin/sh

###
### Script to install pip packages for local development
###
### Assumes you have an active venv
###

# Install local packages for testing
echo "Installing pip packages"
python3 -m pip install pytest
