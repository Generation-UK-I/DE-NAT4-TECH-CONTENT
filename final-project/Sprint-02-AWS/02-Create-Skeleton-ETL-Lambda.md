# Create Skeleton ETL Lambda

## Description

Now that we are moving our PoC to the cloud, we need to create a lambda in AWS that will _eventually_ run our ETL code. For now, it will just log "hello team" when executed.

To get this to work, we need to create all resources using CloudFormation rather than making them manually in the AWS console.

You will need:

- A deployment script
- A deployment bucket stack, called something like "team-name-deployment-stack"
  - with only a deployment bucket in it
- An ETL stack, called something like "team-name-etl-stack"
  - which contains:
  - An s3 bucket for csv files
  - An s3 bucket trigger
  - A basic ETL Lambda (see below)
- Your basic ETL lambda should be called something like "team-name-etl-lambda"
For now the only code it needs is to print("hello team")​ in the entry lambda_hander function
(more code is added in the next story!)

## Additional Requirement

- Your local POC (proof of concept) pipeline for a local test file into local postgres must continue to work independently of what is running in AWS,
  - as must your local unit tests
- This is really useful for debugging the sample data files we get in AWS from different branches
- Consider splitting your local pipeline files out into smaller modules for re-use
- Consider having a different file for the main lambda code vs running locally

## User Story

**As** the business
**I want** to make sure our code is run in the cloud using IaC (Cloudformation)
**So that** it is easy to maintain and cheap to run

## Acceptance Criteria

- [ ] todo
- [ ] todo
- [ ] todo
