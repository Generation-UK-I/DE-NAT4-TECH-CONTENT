###
### PowerShell Script to deploy S3 bucket + lambda in cloudformation stack
###

# Equivalent of set -e command on bash. Exits the script when an error occurs
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

#### CONFIGURATION SECTION ####
$aws_profile=$args[0] # e.g. sot-academy, for the aws credentials
$your_name=$args[1] # e.g. rory-gilmore (WITH DASHES), for the stack name
$team_name=$args[2] # e.g. la-vida-mocha (WITH DASHES), for the database name

$deployment_bucket="$your_name-shopper-deployment-bucket"

# EC2 config
$ec2_ingress_ip=$args[3] # e.g. 12.34.56.78 (of your laptop where you are running this)

# PowerShell may need to directly be opened in the handouts folder for this session for this command to work
$ec2_userdata = [System.Convert]::ToBase64String([System.IO.File]::ReadAllBytes('./userdata'))
#### CONFIGURATION SECTION ####

# Create a deployment bucket stack to hold our zip files of lambdas
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

# Create an updated ETL packaged template "etl-stack-packaged.yml" from the default "etl-stack.yml"
# ...and upload local resources to S3 (e.g zips files of your lambdas)
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
      YourName=$your_name `
      TeamName=$team_name `
      EC2InstanceIngressIp=$ec2_ingress_ip `
      EC2UserData=$ec2_userdata;
      
Write-Output ""
Write-Output "...all done!"
Write-Output ""
