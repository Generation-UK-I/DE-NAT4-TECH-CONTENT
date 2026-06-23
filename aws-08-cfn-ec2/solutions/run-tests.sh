#!/bin/sh

###
### Script to run local unit tests with pytest
###

echo "Running pytest..."

# Windows users in GitBash may need to use "python" instead of "python3" due sto the venv
python3 -m pytest -v -s
