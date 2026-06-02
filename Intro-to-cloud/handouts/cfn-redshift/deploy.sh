#!/bin/sh
set -eu

#### CONFIGURATION SECTION ####
aws_profile="$1" # e.g. sot-academy, for the aws credentials
team_name="$2" # e.g. 'la-vida-mocha' USE YOUR TEAM NAME FOR THIS SESSION - WITH DASHES
deployment_bucket="${team_name}-shopper-deployment-bucket"
#### CONFIGURATION SECTION ####

# Create deployment bucket stack
echo ""
echo "Doing deployment bucket..."
echo ""
aws cloudformation deploy --stack-name "${team_name}-shopper-deployment-bucket" \
    --template-file deployment-bucket-stack.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM --profile ${aws_profile} \
    --parameter-overrides \
      TeamName="${team_name}";

# If SKIP_PIP_INSTALL variable is not set or is empty then do a pip install
if [ -z "${SKIP_PIP_INSTALL:-}" ]; then
    echo ""
    echo "Doing pip install..."
    # Install dependencies from requirements-lambda.txt into src directory with python 3.12
    # On windows may need to use `py` not `python3`
    python3 -m pip install --platform manylinux2014_x86_64 \
        --target=./src --implementation cp --python-version 3.12 \
        --only-binary=:all: --upgrade -r requirements-lambda.txt;
else
    echo ""
    echo "Skipping pip install"
fi

# Create an updated ETL packaged template "etl-stack-packaged.yml" from the default "etl-stack.yml"
# ...and upload local resources to S3 (e.g zips files of your lambdas)
# A unique S3 filename is automatically generated each time
echo ""
echo "Doing packaging..."
echo ""
aws cloudformation package --template-file etl-stack.yml \
    --s3-bucket ${deployment_bucket} \
    --output-template-file etl-stack-packaged.yml \
    --profile ${aws_profile};

# Deploy the main ETL stack using the packaged template "etl-stack-packaged.yml"
echo ""
echo "Doing etl stack deployment..."
echo ""
aws cloudformation deploy --stack-name "${team_name}-shopper-etl-pipeline" \
    --template-file etl-stack-packaged.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile ${aws_profile} \
    --parameter-overrides \
      TeamName="${team_name}";

echo ""
echo "...all done!"
echo ""
