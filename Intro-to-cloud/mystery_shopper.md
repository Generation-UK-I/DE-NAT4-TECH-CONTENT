# The Mystery Shopper ETL

Before we migrate our final project pipelines to AWS, our client SuperCafe would like us to build a similar data pipeline focusing on mystery shop data from their branches.

> Mystery shopping is a method used by retail companies to help measure job performance and the quality of service being delivered to customers. Typically, a mystery shopper will pay a visit to a branch or store, mirroring the behaviours of a real customer and then submitting scores or feedback about their experience.

SuperCafe have identified some newly opened branches where quality of service could increase, and have introduced mystery shopping in order monitor and help improve customer experience.

Similarly to the sales pipeline we are building, SuperCafe are recording the outcomes of mystery shop visits in CSV files:

- The CSV is uploaded at the end of each month, and represents all visits for the month across all branches in the initiative
- They have provided us a sample CSV containing 5 rows

![mystery-shops](img/mystery-shops-csv.png)<!-- .element: class="centered" height="350px" -->

## The Problem

- It is time consuming to collate data manually on all branches into one CSV
- Gathering meaningful data for the company on the whole is difficult, due to the limitations of the current solution
- Visualising trends is being done manually and is prone to human error
- Integers are represented inconsistently in the data
- `VisitDate` values have to be manually re-formatted to integrate with external spreadsheet software
  - For example some software might expect dates in a different format i.e. MM/DD/YYYY or DD-MM-YYYY

## The Solution

After an initial discovery phase, we have agreed a plan to build a small cloud-based ETL pipeline to help SuperCafe solve some of these issues.

This has been identified as a great opportunity for us to learn and grow as an engineering team before moving onto the sales pipeline for our final project!

## Proposed Pipeline Architecture

This is an overview of how everything might all fit together.

![proposed-arch](./img/data-academy-pipeline-example.e2e.png)<!-- .element: class="centered" height="500px" -->

The Instructors have set up some common networking and a shared RedShift Cluster.

![example-01](./img/data-academy-pipeline-example-shared-01.png)<!-- .element: class="centered" height="500px" -->

These are the parts that are set up. There is one database per Team set up as well:

![example-02](./img/data-academy-pipeline-example-shared-02.png)<!-- .element: class="centered" height="500px" -->


We need to fill in the pieces:

![example-03](./img/data-academy-pipeline-example-shared-03.png)<!-- .element: class="centered" height="500px" -->

### Our first user story

A user story is a short, simple description of a software feature told from the perspective of the end user

`As a` SuperCafe senior manager  
`I want` a durable and available location to store monthly mystery shop data  
`So that` access to the data is securely configured  
`And` the data can be automatically integrated with a downstream ETL pipeline

### Our first user story - Architecture

These are the parts we need to create to meet the story's user acceptance criteria:

![s3.next](img/data-academy-pipeline-example.s3-next.png)<!-- .element: class="centered" height="500px" -->

So we start with this small piece of the whole:

![s3.goal](img/data-academy-pipeline-example.s3-goal.png)<!-- .element: class="centered" height="500px" -->

### Complete the S3 Lab

[S3 Lab](./aws-03-console-s3-exercise.md)

What you did in the lab was this, but manually:

![](img/data-academy-pipeline-example.s3-goal.png)<!-- .element: class="centered" height="500px" -->

So next we need to do it properly, i.e. with Infrastructure as Code.

## Using IaC

After further discussions on the solution for the mystery shopper pipeline, your tech leads have stipulated that we update the original user story to include a new piece of technical acceptance criteria.

Reminder of the current story:

`As a` SuperCafe senior manager  
`I want` a durable and available location to store monthly mystery shop data  
`So that` access to the data is securely configured  
`And` the data can be automatically integrated with a downstream ETL pipeline

### New acceptance criteria

***The S3 bucket used to store the raw mystery shop data should be managed via Infrastructure as Code, so the team can easily manage the automation of creating it in AWS and provide flexibility later if multiple development and production versions of the pipeline are needed.***

> This approach also means the source code for how the bucket is defined can be committed to source control, hurrah!

## Deploying a Stack via the CLI

There is a handy CF plugin for VS Code that can remove some syntax errors we would otherwise get:

![cloudformation-plugin](./img/cloudformation-plugin.png)

- Install the plugin
- Follow the steps to update your YAML editor config

The deploy script you need is done for you, so it will reliably work. If using Linux create a new file called `deploy.sh` and add the following:

```bash
#!/bin/sh
set -eu

###
### Script to deploy S3 bucket in cloudformation stack
###

#### CONFIGURATION SECTION ####
aws_profile="$1" # e.g. sot-academy, for the aws credentials
your_name="$2" # e.g. rory-gilmore (WITH DASHES), for the stack name
#### CONFIGURATION SECTION ####

# Deploy the stack
echo ""
echo "Doing etl stack deployment..."
echo ""
aws cloudformation deploy --stack-name ${your_name}-shopper-etl-pipeline \
    --template-file etl-stack.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM \
    --profile ${aws_profile} \
    --parameter-overrides \
      YourName="${your_name}";

echo ""
echo "...all done!"
echo ""
```

It does the following:

- Collects `aws-profile` and `your-name` from the command line
- Use these to deploy a stack called `your-name-shopper-etl-pipeline`

Here is what the script will deploy:

![AWS-Deployment-script-intro-cfn](./img/AWS-Deployment-script-intro-cfn.png)






---

We have a Template that defines our Resources:

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  MysteryShopper S3 Cloudformation example for AWS week in the Data Engineering Software Academy

Parameters:
  YourName:
    Type: String
    Description: Enter your name in format 'first-last' to customise the way your resources are named
    Default: rory-gilmore

Resources:
  ShopperRawDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${YourName}-shopper-raw-data'
      PublicAccessBlockConfiguration: # do not allow any public access
        BlockPublicAcls: True
        BlockPublicPolicy: True
        IgnorePublicAcls: True
        RestrictPublicBuckets: True
      Tags:
        - Key: Name
          Value: !Sub '${YourName}-shopper-raw-data'

  ShopperRawDataBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref ShopperRawDataBucket
      PolicyDocument:
        Statement:
          - Sid: "AllowSSLRequestsOnly"
            Action: "s3:*"
            Principal: "*"
            Effect: "Deny" # Block if...
            Resource:
              - !Sub "arn:aws:s3:::${YourName}-shopper-raw-data"
              - !Sub "arn:aws:s3:::${YourName}-shopper-raw-data/*"
            Condition:
              Bool:
                aws:SecureTransport: "false" # ...the request is not HTTPS

```

How do we turn that template into a stack in AWS?

There are two main options:

1. Deploy via AWS Web Console
2. Deploy via the AWS Command Line Interface (CLI)
    - the preferred way, we can automate this!

### Console Deployment

A stack can be created by uploading a template file via the Web interface, by going to:

AWS Web Console > `CloudFormation` -> `Stacks` -> `Create Stack`

While a stack is deploying, the web console can be used to see what is happening, and to check what resources have been created.

**DEMO**

