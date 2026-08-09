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

## Our first user story

A user story is a short, simple description of a software feature told from the perspective of the end user

`As a` SuperCafe senior manager  
`I want` a durable and available location to store monthly mystery shop data  
`So that` access to the data is securely configured  
`And` the data can be automatically integrated with a downstream ETL pipeline

### Architecture

These are the parts we need to create to meet the story's user acceptance criteria:

![s3.next](img/data-academy-pipeline-example.s3-next.png)<!-- .element: class="centered" height="500px" -->

So we start with this small piece of the whole:

![s3.goal](img/data-academy-pipeline-example.s3-goal.png)<!-- .element: class="centered" height="500px" -->

You've already deployed some buckets through the Management Console, and added some objects to them, but in this case we want to deploy using industry best practices i.e. Infrastructure as Code (IaC).

### Using IaC

After further discussions on the solution for the mystery shopper pipeline, your tech leads have stipulated that we update the original user story to include a new piece of technical acceptance criteria.

**New acceptance criteria: The S3 bucket used to store the raw mystery shop data should be managed via Infrastructure as Code, so the team can easily manage the automation of creating it in AWS and provide flexibility later if multiple development and production versions of the pipeline are needed.**

> This approach also means the source code for how the bucket is defined can be committed to source control, hurrah!

## Console Deployment

A stack can be created by uploading a template file via the Web interface, by navigating to:

`AWS Management Console` > `CloudFormation` -> `Stacks` -> `Create Stack`

While a stack is deploying, the web console can be used to see what is happening, and to check what resources have been created.

## CLI Deployment

For speed, consistency, easier version control, and many other benefits, we are going to use the CLI. But first we need to complete our deployment template.

There is a handy CF plugin for VS Code that can remove some syntax errors we might encounter when writing CloudFormation templates:

![cloudformation-plugin](./img/cloudformation-plugin.png)

- Install the plugin
- Follow the steps to update your YAML editor config

### The Deployment Script

As you have seen, when you deployed the AWS CLI we gained a whole range of AWS specific commands, typically in the format `aws <service> <operation> <options> <arguments>`, and this includes a range of commands for working with CloudFormation, including deploying stacks.

This works fine for individual stacks, but in complex enterprise environments deployments may comprise multiple stacks, along with various files, data, function code, and other resources.

For this reason it is common to create a Bask script which can handle the CloudFormation deployment automatically, including passing through any required files and values, as well as embedding some progress messages and error handling.

Our deployment, and the deployment script, will become complex, therefore we have provided it for you for each story so it will reliably work, and you won't need to worry about it during any necessary troubleshooting.

It is recommended that you compare the different versions of the script as you come across them to identify the differences.

Below is the first version of the **deploy** script.

We will be deploying from our Linux VM, therefore create a new working directory for the project, and a new file within called `deploy.sh`. Open the file with your preferred text editor (e.g. nano) and add the following

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

Here's what the script does:

- Collects `aws-profile` and `your-name` from the command line
  - `your-name` should be entered `lower-case-with-dashes`, as it will be used in the S3 Bucket names
- Use these to deploy a stack called `your-name-shopper-etl-pipeline`, which is defined in a file called `etl-stack.yml`.
  - Notice that the deployment is initiated by running the `aws cloudformation deploy...` command within the script, including all of our required options and arguments.

>Remember, your `aws-profile` authenticates you; You created it when following the [aws-account-setup](./aws-account-setup.md) guide.
>
>When you start a new session you authenticate your SSO profile with `aws sso login --profile=<profile-name> --use-device-code`. After authentication you can then use your profile to authenticate your AWS commands.

### The CloudFormation Template

Here is the `etl-stack.yml` file, for easier editing you may wish to work with it in VSC, then copy it to your Linux VM when you're ready to deploy.

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
  # TODO add ShopperRawDataBucket
  # TODO Add ShopperRawDataBucketPolicy
```

### Completing the First Story

**Notice we're missing our resources**: Completing these is your next task. You should reference the [intro-to-iac guide](./intro-to-iac.md), and the [AWS CloudFormation reference page](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-template-resource-type-ref.html)

>As you can see in the template, the parameter for `YourName` is already done, so no-one forgets it
>
>This is passed in from the deployment script.

Here is what should happen when you run the script, and deploy the stack:

![AWS-Deployment-script-intro-cfn](./img/AWS-Deployment-script-intro-cfn.png)

**TODO: Complete the first story** by adding each of the following sections to the etl-stack template. Expand each section to reveal its' requirements. You should reference the provided resources, and the CloudFormation reference page to figure out how to structure the YAML blocks.**

<details><summary>Add a bucket with a dynamic name:</summary>

- Needs a `Resources` section
- Then a logical name e.g. `ShopperRawDataBucket`, to use within the template
- Then an AWS `Type`, e.g. `AWS::S3::Bucket`, which must be a valid value from the AWS reference docs
- Then some `Properties`, which is a key to hold more values

</details>

<details><summary>Bucket properties:</summary>

These match what we saw in the AWS console in the last session; They all sit under the `Properties` key:

- A globally-unique `BucketName`, so we know which one is ours
- A set of `PublicAccessBlockConfiguration`(s), for security
  - By default, deny all public access!
- A `Name` Tag with a `Key` and `Value`, so it is labelled correctly as ours

</details>

<details><summary>Add policy:</summary>

Add a bucket policy with dynamic references.

- A logical name e.g. `ShopperRawDataBucketPolicy`, within the `Resources` section
- A specific `Type`, e.g. `AWS::S3::BucketPolicy`
- A set of `Properties`
  - With a dynamic reference back to our Bucket, e.g. `Bucket: !Ref ShopperRawDataBucket`
  - A `PolicyDocument` detailing our security rules (in this case - to make sure only secure traffic on HTTPS can be used, not HTTP)

</details>

</details>

<details><summary>Add Policy Document:</summary>

These define the security rules for the Policy and are provided as a policy **parameter**:

- A `Statement` block
- With an identifier `Sid`, which is like a unique human-readable name for the Statement
- Then an `Action`, to define what the rules apply to, like `s3:PutObject` or `s3:DeleteObject`, or `s3:*` for "all"
- A `Principal`, which is _who_ the rule applies to or "*" for everyone
- The `Effect`, which is `Allow` or `deny`
- A list of AWS `Resource`(s), that the rule is guarding / protecting
- Any `Condition`(s), that turn the rule on or off

</details>

#### Sample Solution

<details><summary>Reveal:</summary>

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

</details>

## AWS Lambda

Proceed after completing: aws-05-intro-lambda.md

## Our Second User Story

Lets revisit our Mystery Shopper target setup:

![data-academy-pipeline-example](img/data-academy-pipeline-example.e2e.png)<!-- .element: class="centered" height="500px" -->

`As a` SuperCafe senior manager  
`I want` the Mystery Shopper data processed automatically  
`So that` the data can be analysed  
`And` the pipeline can run daily

### Architecture

Now that we know Lambda a bit, we will deploy a Lambda "properly" using IaC:

![lambda-next](img/data-academy-pipeline-example.lambda-next.png)<!-- .element: class="centered" height="500px" -->

We have coded a Lambda function for you so we can set it up with IaC.

These are the pieces we will need:

![lambda-goal](img/data-academy-pipeline-example.lambda-goal.png)<!-- .element: class="centered" height="500px" -->

This is a complex process with a few stages:

![cloudformation-deployment](img/cloudformation-deployment.svg)<!-- .element: class="centered" height="350px" -->

### S3 Deployment Bucket

Our lambda code can get very big, especially with added dependencies. It is common practice to do the following when deploying lambdas from IaC:

- Install any dependencies locally, into the same folder as our python code
- Zip up the Lambda code folder, including the above dependencies
- Upload the Zip to a **Deployment Bucket**
- The Lambda is then deployed from the Zip in the Deployment bucket into the Lambda service

This process is known as a **zip deployment**

### Packaging with CloudFormation

Packaging is the act of getting CloudFormation to:

- Bundle our Lambda code into Zip files,
- Upload the zip files somewhere ready to use later (S3)
- Update our template YAML files to point to the Zip, so that CF knows what to do in AWS

>The next version of the [deploy.sh](./handouts/cfn-lambda/deploy.sh) script in the [./handouts/cfn-lambda/](./handouts/cfn-lambda/) folder will package a lambda function for you once all of the necessary files and resources are in place.

Getting our local code to Lambda has two stages:

1. The package stage involves zipping local code files (if the stack points to them) and uploading it to an S3 bucket
    - The source stack file will refer to local files e.g. a folder like `./src` that will not exist in AWS
    - The Template must be "packaged" to fix this
    - So, "Packaging" uploads a zip of the lambda code S3,
    - Then copies the template file and replaces local paths like `./src` with S3 URIs (protocol and bucket name and key) like `s3://my-deployment-bucket/abc-def-my-zip-file`
2. The deployment stage involves deploying a CloudFormation stack based on the *packaged* template file (with the new paths in it)

To complete our next story we need to start from the previous `etl-stack.yml` file. If you completed Story 1 you may use your own, otherwise the next version is here, including prompts for where your next elements need to be added.

- [etl-stack.yml](./handouts/cfn-lambda/etl-stack.yml)

Additionally, remember, our task is to understand CloudFormation deployments, so we don't need to dissect the Lambda function code, therefore this is also provided, along with some sample data.

- [deploy.sh](./handouts/cfn-lambda/deploy.sh)
- [sample data](./handouts/cfn-lambda/mystery_shops_2024-03.csv)

As before, you will need to complete the etl-stack.yml.

### Networking

The network, over which the components of our app will communicate, already exists - here's a recap of it from a previous session.

![data-academy-pipeline-example-shared-03.png](./img/data-academy-pipeline-example-shared-03.png)<!-- .element: class="centered" height="500px" -->

We will add settings in the upcoming slides to put our Lambda in the same place as the Redshift cluster, so it can access it:

### Completing Story 2

Our `etl-stack.yml` requires a **parameter** for `NetworkStackName`, so we know where to put the lambda (so that in a later session it can talk to RedShift).

Add a section to the template...

- In the `Parameters` section
- With logical name `NetworkStackName`
  - With a `Type` of `String`
  - A `Default` value of `project-networking`
  - And a helpful `Description`

`project-networking` is the CF stack containing networking resources to communicate with Redshift. We are setting a parameter for the network stack to reference the `project-networking` stack later.

<details><summary>Reveal:</summary>

```yaml
Parameters:
  YourName: # This parameter already exists
    Type: String
    Description: Enter your name in format 'first-last' to customise the way your resources are named

  NetworkStackName: # Need to add this one
    Type: String
    Default: project-networking
    Description: Network stack with VPC containing Redshift instance
```

</details>

>The template adds the `project-networking` tag to each of the deployed elements; **Tagging** allows you to add key-value pairs as metadata against your resouces; In the Management Console you can use **AWS Resource Explorer** to search for all resource with a particular tag - *you do not have access to this service on your current profile*.

Next we require a Lambda with a dynamic name (passed from `YourName`), so all our lambdas are unique. It should be...

- In the `Resources` section
- With a logical name like `EtlLambdaFunction`
- And a specific `Type` of `AWS::Lambda::Function`
- And many `Properties`, we need at least the following, although there are many that we can set:
  - A unique and dynamic `FunctionName`, using `YourName`
  - An up to date `Runtime`, `python3.12`
  - A `Handler` to specify the file name and function name to run
  - The `Code` setting, to specify which folder our source code is in e.g. `./src`
  - A `Role`, to assume for security so we are allowed to talk to RedShift and the S3 bucket
  - A `Timeout` value in seconds e.g. `30`, high enough for our E-T-L to run but not time out
  - A `VpcConfig`, to put our lambda in the same networking as RedShift so it can see the DB
  - A `Tag` with value `Name` to further identify our lambda

<details><summary>Reveal:</summary>

```yaml
Resources:
  EtlLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${YourName}-shopper-etl-lambda'
      Runtime: python3.12
      Handler: mystery_shop_etl_lambda.lambda_handler # file_name.function_name
      Role: !Sub 'arn:aws:iam::${AWS::AccountId}:role/lambda-execution-role' # security rule
      Timeout: 30 # max running time in seconds (make as low as possible)
      ReservedConcurrentExecutions: 10 # how many can run at once
      Code: ./src # use this folder for the zip of lambda code
      VpcConfig: # use the same networking as RedShift
        SecurityGroupIds:
          - Fn::ImportValue:
              !Sub '${NetworkStackName}-VPCSGID'
        SubnetIds:
          - Fn::ImportValue:
              !Sub '${NetworkStackName}-PrivateSubnet0ID'
      Tags:
        - Key: Name
          Value: !Sub '${YourName}-shopper-etl-lambda'
```

</details>

Next we need to configure how to wake (or *trigger*) the Lambda function, by adding a **Notification Configuration** to the CSV data bucket, so that files arriving there wake up the lambda.

We need to extend the `ShopperRawDataBucket` configuration `Properties`, like so:

- Add a new `NotificationConfiguration` property
- With a child property of `LambdaConfigurations`
  - This has a child list of Event & Function tuples
  - Add an `Event` of type `s3:ObjectCreated:*`
  - With a `Function` (lambda) reference to `!GetAtt EtlLambdaFunction.Arn`

<details><summary>Reveal:</summary>

```yaml
Resources:
  EtlLambdaFunction:
    Type: AWS::Lambda::Function
    ...
  ShopperRawDataBucket:
    Type: AWS::S3::Bucket
    ...
      NotificationConfiguration: # Add this block to trigger the lambda when a file is added
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Function: !GetAtt EtlLambdaFunction.Arn
```

</details>

We should also tell CloudFormation that the Bucket **DependsOn** the permissions and the Lambda, so it will not deploy until it's required dependencies are created first.

```yaml
  ShopperRawDataBucket:
    ...
    DependsOn:
      - ShopperRawDataBucketPermission
      - EtlLambdaFunction
```

Most of the time, CloudFormation will work these out for itself. However we have found in this stack, the build order is more reliable with this hint added.

Finally we also need to add a **Source Bucket Permission**, so the Lambda is allowed to read from the bucket when it is invoked.

- We need a new `Resource` called `ShopperRawDataBucketPermission`
- With a `Type` of `AWS::Lambda::Permission`
- The `Properties` of it are
  - An `Action`, which is `lambda:InvokeFunction`, for when the lambda is activated
  - The `FunctionName`, by reference to our lambda, e.g. `!Ref EtlLambdaFunction`
  - For the specific `Principal` that is `s3.amazonaws.com`
  - Allowing the `SourceArn` by name so `!Sub 'arn:aws:s3:::${YourName}-shopper-raw-data'`

<details><summary>Reveal:</summary>

```yaml
Resources:
  ...
  ShopperRawDataBucketPermission: # allow the triggered lambda to read from the bucket
    Type: AWS::Lambda::Permission
    Properties:
      Action: lambda:InvokeFunction
      FunctionName: !Ref EtlLambdaFunction
      Principal: s3.amazonaws.com
      SourceArn: !Sub 'arn:aws:s3:::${YourName}-shopper-raw-data'
```

</details>

### Deploy the New Stack

To deploy the script we have provided a solution to all of the above steps for you, including the **etl-stack** and a separate **deployment-bucket.yml** template, along with the Lambda code, all in the correct structure. Find this in the [solution.zip](./handouts/cfn-lambda/solution/solution.zip) file, in the [/handouts/cfn-lambda/solution/](./handouts/cfn-lambda/solution/) directory.

This also includes the next version of the `deploy.sh` file, which will package the lambda function for you during deployment.

The easiest approach will be to copy the solution.zip file into your VM using SCP, e.g. `scp solution.zip centos@[VM_IP]:/home/centos/`.

Unpack the solution.zip file in a new working directory, and unpack it with `unzip solution.zip` and review the sample files.

>If you do not have the unzip utility you can install it with `sudo yum install unzip -y`

Once upacked you can use the provided `etl-stack.yml`, or try using your own template if you completed the previous Story (*compare the two before using your own*).

The structure of the resources should be like this:

```bash
[new_directory]
      |
      |-deploy.sh
      |-etl-stack.yml
      |-deployment-bucket.yml
      |-requirements-lambda.txt # Create this empty txt file
      |-[src]
          |-mystery_shop_etl_lambda.py
```

With the necessary files in place we can try deploying the stack(s).

1. If not already done, initiate an SSO session with `aws sso login --profile=<profile_name> --use-device-code`, and authenticate your device on our SSO sign in page (https://aws-generation.awsapps.com/start/#/device) using the provided code.
2. The deploy.sh script requires two parameters aws_profile and your_name, type the following to run the script, and provide these parameters: ``

```bash
bash deploy.sh <aws-profile> <your-name>
```

- `aws-profile`: the 'friendly' name you chose when configuring your SSO profile
- `your-name`: your name in the format 'first-last'
  - Dashes not underscores as it will be part of your bucket names

Here is what the script does:

- Collect your `aws-profile` and `your-name` from the command line
- Deploy a stack called `your-name-shopper-deployment-bucket`
- Install the Lambda's dependencies in the `src` folder
- Package the `your-name-shopper-etl-pipeline` stack with a Lambda Zip in S3
- Deploy a stack called `your-name-shopper-etl-pipeline`

3. Monitor your deployment for errors - it can take a few minutes

>If you receive an error like `deploy.sh: line 22: $'\r': command not found`, then you have a 'CRLF' issue, you can fix it with the `dos2unix` utility

4. Once complete log into the management console via our login portal and navigate to the Lambda, CloudFormation, and S3 consoles to locate your deployed resources.
5. Upload the `mystery_shops_2024-03.csv` file to your `...RawData...` bucket. This should trigger your lambda.
6. Find your Log Group in CloudWatch and check the latest Log Stream. You should see some nice useful logs.

Here is what the script deployed:

![AWS-Deployment-script-full-stack-cfn-next-session](./img/AWS-Deployment-script-full-stack-cfn-next-session.png)

## AWS RedShift

Proceed after reviewing: intro-to-dw.md

## Our Third user Story

`As a` SuperCafe senior manager  
`I want` the Mystery Shopper data to be analysed  
`So that` we can award the friendliest most helpful store a prize each month

### Architecture

We want to check our data is going into the database, so that we can query it.

![](img/data-academy-pipeline-example.redshift-next.png)<!-- .element: class="centered" height="500px" -->

So for now we only need this chain of parts to be working:

![](img/data-academy-pipeline-example.redshift-goal.png)<!-- .element: class="centered" height="500px" -->

This session does not involve a new CloudFormation _per-se_ - rather, using tools already in our toolbox, we connect to RedShift, add data, and query it.

So that we can focus upon understanding and using RedShift, the ETL Lambda python code is provided for you, and has been extended to talk to RedShift for us.

Now we've learned a little bit about Amazon Redshift, let's implement loading some data from the Mystery Shopper pipeline into a database hosted on a Redshift cluster.

The key files required are:

- See [./handouts/cfn-redshift/src/mystery_shop_etl_lambda.py](./handouts/cfn-redshift/src/mystery_shop_etl_lambda.py)
- And [./handouts/cfn-redshift/src/utils/db_utils.py](./handouts/cfn-redshift/src/utils/db_utils.py)
- And [./handouts/cfn-redshift/src/utils/sql_utils.py](./handouts/cfn-redshift/src/utils/sql_utils.py)

Spend some time reviewing these files, and see if you can follow the logic and figure out what they're doing.

### Connecting to RedShift

For convenience, consistency, and cost effectiveness, a single RedShift cluster has been created for you, along with an individual database for each team, within the cluster which will act as the target for your ETL pipeline.

This means that the final deployment to create the pipeline which connects to RedShift, creates your DB tables, and deploys the Lambda ETL function, should be done by just one team member. The other members can then all use the pipeline once deployed.

The RedShift connection details will be in a **Parameter Store** parameter called `<team_name>_redshift_settings` (Parameter Store prefers underscores '_' not dashes)

Your **team names** are the ones you chose for your main project, but the format will comprise a bucket name, so if the team name is 'Best Coffee Shop' for the deployment enter `best-coffee-shop` where prompted.

---

### Parameter Store

AWS provides a service for managing your deployed infrastructure called Systems Manager (SSM). One of the utilities provided by SSM is Parameter Store in which you can store values, which can then be accessed programmatically i.e. from within an app.

This provides a few important benefits:

- Avoids having to hard-code credentials or sensitive info within application code, or store them as environment variables within the system.
- Multiple systems can access the same parameter, which avoids having to enter the info in several locations.
- If the value needs to be changed, it only needs to change in one place.

This is particularly useful for values such as usernames, connection endpoints, IP addresses, and so on.

>Secrets Manager is another service which offers similar functionality, but it includes the ability to automatically rotate sensitive credentials such as passwords or encryption keys.
>
>Systems Manager also allows for much larger secrets to be stored.

---

### Our Next Deployment script

The deploy script `deploy.sh` in the [./handouts/cfn-redshift/](./handouts/cfn-redshift/) folder are done for you, so they will reliably work.

It does the following:

- Collects `aws-profile` and `team-name` from the command line
- Deploy a stack called `team-name-shopper-deployment-bucket`
- Install the Lambda's dependencies in the `src` folder
- Package the `team-name-shopper-etl-pipeline` stack with Lambda Zip in S3
- Deploy a stack called `team-name-shopper-etl-pipeline`

Here's what the script will deploy:

![AWS-Deployment-script-full-stack-cfn-deployables](./img/AWS-Deployment-script-full-stack-cfn-deployables.png)

### Deployment and Querying

For each team nominate a driver to screen share their terminal and AWS console view, and then work through the steps below as a group.

### Deployment

All of the required files are in the [cfn-redshift.zip](./handouts/cfn-redshift/cfn-redshift.zip) in the [./handouts/cfn-redshift/](./handouts/cfn-redshift/) folder.

This ZIP file should be copied to a new working directory within your centos VM (using SCP), and unzipped. At this point you may try replacing the provided `etl-stack.yml` file with your own if you finished Story 2, otherwise you can use the sample.

>Only ONE person should do this with the rest of the team watching

In your VM, with the required files and structure in place:

1. Log into AWS if not already done so (`aws sso login --profile=de-nat4-admin --use-device-code`)
2. Deploy the script with `bash deploy.sh <aws-profile> <team-name-with-dashes>`
    - eg `bash deploy.sh ant-de-profile best-coffee-shop`

This script does the following:

- Updates our **SSM** parameter environment variable via etl-stack.yml changes
- Adds new python code to handle querying the SSM parameter from **Parameter Store**
- Adds new python code to connect to the redshift database:
- Creates our our `mystery_shop_visit` table if it doesn't already exist
- Inserts our transformed data into the table

Observe the deployment, wait until the script has finished updating the stack.

>The rest of the team may carry out the following steps.

Log into the Management Console and open the `CloudFormation` page in the AWS console and locate your team's stack, e.g `best-coffee-shop-etl-pipeline`

- Find the the `Resources` tab
  - In it, open the link to your S3 `raw-data` bucket, e.g. `best-coffee-shop-shopper-raw-data`
  - Then upload a copy of `mystery_shops_2024-03.csv` from the `handouts/data` folder
- Back the `Resources` tab, click the link to your ETL Lambda, e.g. `best-coffee-shop-shopper-etl-lambda`
- Navigate the lambda user interface to confirm:
  - The new SSM environment variable has been added
  - The lambda code has now been updated to include the redshift logic
  - The lambda was invoked after you dropped the CSV into the `raw-data` bucket
- Open the cloudwatch logs for your lambda and inspect the log output
  - Look for the most recent log stream, and open it
  - Confirm the redshift logic was executed successfully (no errors!)

### Querying the RedShift Database

Now we can try querying our data in RedShift.

Navigate to the *Amazon Redshift* web console:

- Click on the running cluster under `Cluster overview` on the main homepage
- Under the `Query data` dropdown on the top right, select `Query in query editor v2`
- There should be a dropdown on the top left named `redshiftcluster-*****`
  - click the three dots on it
  - and select, `Edit connection`, or `Create connection`
- Under `Other ways to connect`, ensure the `Database user name and password` option is selected
- Open the AWS Service Manager console in another browser tab
  - Find the `Parameter Store` in the left bar
  - Navigate to the parameter called `<your-team-name>_redshift_settings` to find your redshift credentials
    - e.g `best-coffee-shop_redshift_settings`
    - You should be able to see your DB name, DB user name and DB password
- Back in the Redshift user interface,
  - Enter the `Database`, `User name` and `Password` values
  - Click `Save`
- Expand the list of databases under the redshift cluster name
  - Click on your DB name
- Expand the list of Tables for your database
- Access your team's table in the list on the left
  - The tables created by your python lambda code can be viewed under `Public > Tables`
  - You can right-click on your table name and choose the menu option "Select table"
- In the main SQL window, have a go at writing and running some sql queries for your `mystery_shop_visit` table,
  - Make sure your team's database is selected in the dropdown at the top next to `redshiftcluster**`.
- Start with `SELECT * FROM mystery_shop_visit;`
- Make a query for "Display Store name by Rating"
  - Some sample SQL could be
    - `SELECT m.store_name, m.overall_score FROM mystery_shop_visit m ORDER BY m.store_name;`
    - And also
      - `SELECT m.store_name, MAX(m.overall_score) AS max_score FROM mystery_shop_visit m GROUP BY m.store_name ORDER BY max_score desc;`

---

At this point you have a functional ETL pipeline which inserts data into a data-warehouse, and you have demonstrated running SQL queries to perform some simple analysis.

You should try to adapt what you have learned through this mystery shopper mini-project to apply the same functionality to your main project.

### Optional extra task

> In your own project / exercise time, change your code to do a bulk insert with ['execute_values()'](https://www.psycopg.org/docs/extras.html#fast-execution-helpers).

This will be useful for performance in the Team Projects when inserting large amounts of data from multiple files.

You can refer back to the databases resources for this.
