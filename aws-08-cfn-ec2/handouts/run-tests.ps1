###
### PowerShell Script to run local unit tests with pytest
###

Write-Output "Running pytest..."
python -m pytest -v -s
