###
### PowerShell Script to deploy S3 bucket + lambda in cloudformation stack
###

# Equivalent of set -e command on bash. Exits the script when an error occurs
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

#### CONFIGURATION SECTION ####
$aws_profile=$args[0] # e.g. sot-academy, for the aws credentials
$your_name=$args[1] # e.g. rory-gilmore (WITH DASHES), for the stack name
$deployment_bucket="$your_name-shopper-deployment-bucket"
#### CONFIGURATION SECTION ####

# Create deployment bucket stack
Write-Output ""
Write-Output "Doing deployment bucket..."
Write-Output ""
aws cloudformation deploy `
    --stack-name $deployment_bucket `
    --template-file deployment-bucket-stack.yml `
    --region eu-west-1 `
    --capabilities CAPABILITY_IAM `
    --profile $aws_profile `
    --parameter-overrides `
      YourName=$your_name;

# If SKIP_PIP_INSTALL variable is not set or is empty then do a pip install
if (-not $SKIP_PIP_INSTALL) {
    Write-Output ""
    Write-Output "Doing pip install..."
    # Install dependencies from requirements-lambda.txt into src directory with python 3.12
    # On windows may need to use `py` not `python3`
    python3 -m pip install `
        --platform manylinux2014_x86_64 `
        --target=./src `
        --implementation cp `
        --python-version 3.12 `
        --only-binary=:all: `
        --upgrade -r requirements-lambda.txt;
}
else {
    Write-Output ""
    Write-Output "Skipping pip install"
}

# Package template and upload local resources to S3
# A unique S3 filename is automatically generated each time
Write-Output ""
Write-Output "Doing packaging..."
Write-Output ""
aws cloudformation package `
    --template-file etl-stack.yml `
    --s3-bucket $deployment_bucket `
    --output-template-file etl-stack-packaged.yml `
    --profile $aws_profile;

# Deploy template pointing to packaged resources
Write-Output ""
Write-Output "Doing etl stack deployment..."
Write-Output ""
aws cloudformation deploy `
    --stack-name "$your_name-shopper-etl-pipeline" `
    --template-file etl-stack-packaged.yml `
    --region eu-west-1 `
    --capabilities CAPABILITY_IAM `
    --profile $aws_profile `
    --parameter-overrides `
      YourName=$your_name;
      
Write-Output ""
Write-Output "...all done!"
Write-Output ""
