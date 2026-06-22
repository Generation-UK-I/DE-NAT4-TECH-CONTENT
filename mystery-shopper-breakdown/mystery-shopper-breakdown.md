# Mystery Shopper > Final Project

In brief, your final project requires you to build an ETL pipeline which will take a RAW data csv, extract and parse the data, then insert it into a database in a data warehouse.

There is an extra layer of complexity however, because in the interests of creating a production-like product, we aim to automate using IaC as much as possible.

Your first project provided you with a solid foundation of understanding around how Python can interact with databases, but even with this experience, the complexity of your final project is still a big step up.

To support you with this task we have provided you with the Mystery Shopper mini-project, which contains many of the same actions which you can adapt and reuse, but to do that you need to understand what it does and how it works in the first place.

That is our objective now.

## Mystery Shopper Files and Resources

The components for the Mystery Shopper Pipeline (MSP) are laid out as follows

```text
[app_dir]
    |-[src]
    |   |-[utils]
    |   |    |- db_utils.py
    |   |    |- s3_utils.py
    |   |    |- sql_utils.py
    |   |- etl.py
    |   |- mystery_shop_etl_lambda.py
    |- deployment-bucket-stack.yml
    |- deploy.sh
    |- etl-stack-packaged.yml
    |- etl-stack.yml
    |- requirements-lambda.txt
    |- requirements-test.txt
```

To commence our deployment we run the `deploy.sh` bash script, so let's start there.

__deploy.sh:__

```bash
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
```

__Breakdown:__

```bash
# comments omitted
aws_profile="$1"
team_name="$2"
deployment_bucket="${team_name}-shopper-deployment-bucket"
```

When running a script you can pass values through to it, which can be used within your script. The values are automatically mapped to variables, the first value is assigned to $1, the second to $2, and so on.

In our case we pass through your AWS SSO profile to authenticate your commands, and your team name, so execute the script with something like `bash deploy.sh myAwsProfile myTeamName`, then these values are immediately assigned to appropriately named variables (`aws_profile` and `team_name`) for easier use later on.

Next we create a `deployment_bucket` name variable, by adding the team name to a pre-defined string.

```bash
# echo lines omitted
aws cloudformation deploy --stack-name "${team_name}-shopper-deployment-bucket" \
    --template-file deployment-bucket-stack.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM --profile ${aws_profile} \
    --parameter-overrides \
      TeamName="${team_name}";
```

Next we do our first (of two) CloudFormation deployment, we could type this into the CLI manually, but automating it is much more efficient.

Our deployment requires a number of options:

- `stack-name`: a descriptive name for the stack
  - Remember a stack is a logical container for a collection of resources to be deployed, so they may be managed as a group.
- `template-file`: our CloudFormation deployment template
- `region`: the region in which to deploy our stack
- `capabilities`: allows us to provide additional 'capabilities' to our deployed resources, in this case creating or modifying IAM entities.
- `profile`: our profile is our authentication method - if you authenticate via a different method you would not require this parameter.
- `parameter-overrides`: uses a given value in place of an existing parameter from your CF template

If you would prepare to review the `deployment-bucket-stack.yml` CF template now, while you're focused upon this stage, you may do so here [LINK], or proceed to continue reviewing the `deploy.sh` script.

```bash
# If SKIP_PIP_INSTALL variable is not set or is empty then do a pip install
if [ -z "${SKIP_PIP_INSTALL:-}" ]; then
    ...
    # Install dependencies from requirements-lambda.txt into src directory with python 3.12
    # On windows may need to use `py` not `python3`
    python3 -m pip install --platform manylinux2014_x86_64 \
        --target=./src --implementation cp --python-version 3.12 \
        --only-binary=:all: --upgrade -r requirements-lambda.txt;
else
    ...
fi

# NOTE: 'echo' cmds omitted
```

The comments hopefully make the purpose of this section clear, i.e. install required dependencies, however notice that the installation files are being directed to the `./src` directory. This contents of this directory will be packaged and uploaded as our Lambda function, so our required dependencies will also be included.

```bash
# Create an updated ETL packaged template "etl-stack-packaged.yml" from the default "etl-stack.yml"
# ...and upload local resources to S3 (e.g zips files of your lambdas)
# A unique S3 filename is automatically generated each time
...
aws cloudformation package --template-file etl-stack.yml \
    --s3-bucket ${deployment_bucket} \
    --output-template-file etl-stack-packaged.yml \
    --profile ${aws_profile};
```

This block does a lot for us very easily; Our deployment may contain many resources, including yaml templates, our lambda function code, additional YAMLs/JSONs/cfg files for different services, and so on. In this context we call these '_artifacts_'.

- `cloudformation package`: initiates the package operation, taking the following options:
  - `--template-file` your initial stack - the package operation will follow any references in this stack and gather all of the artifacts to include in the package.
  - `--s3-bucket` the bucket to which package can upload all of your artifacts.
  - `--output-template-file`: The package operation replaces local references and paths with links to the artifacts in S3 and returns a new template with the specified file name.
  - `--profile`: authenticates the CLI command

By this point you might be asking "Where is the Lambda function code?", well it's actually referenced by the etl-stack.yml file, so the package operation is going to pick it up for us as an artifact.

It's actually located in the `./src` directory, if you want to dissect it now go here LINK or carry on below to finish breaking down the deploy.sh script.

```bash
# Deploy the main ETL stack using the packaged template "etl-stack-packaged.yml"
...
aws cloudformation deploy --stack-name "${team_name}-shopper-etl-pipeline" \
    --template-file etl-stack-packaged.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile ${aws_profile} \
    --parameter-overrides \
      TeamName="${team_name}";
...
```

The final part of the script is to actually deploy the ETL components based on our new packaged stack template. Most of the options for the `cloudformation deploy` command we've already seen (or are obvious, like `--region`). However to point out the `CAPABILITY_IAM` and `CAPABILITY_NAMED_IAM` statements, these relate to allowing our stack to interact with some of our custom IAM entities that are used to manage our particular cohort's isolated environment.
