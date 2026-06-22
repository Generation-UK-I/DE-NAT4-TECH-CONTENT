# CloudFormation Templates Breakdown

The mystery shopper project requires two different deployments, the first is to create a 'deployment bucket' into which we can add the resources required for our more complex second deployment containing our actual ETL components.

>We could do all of this in one deployment template, using a bunch of `DependsOn` conditions, but this can be un-reliable. This way the first stack must fully complete before commencing the second. Additionally, modularising our deployments, like modularising our code, can allow for easier ongoing development and version control.

---

Here's our first cloudformation template

__deployment-bucket-stack.yml:__

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  Mystery Shopper ETL pipeline example deployment bucket for CF files + Lambda zips

Parameters:
  TeamName:
    Type: String
    Description: Enter your name in format 'first-last' to customise the way your resources are named
    Default: rory-gilmore

Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${TeamName}-shopper-deployment-bucket'
      PublicAccessBlockConfiguration: # do not allow any public access
        BlockPublicAcls: True
        BlockPublicPolicy: True
        IgnorePublicAcls: True
        RestrictPublicBuckets: True
      Tags:
        - Key: Name
          Value: !Sub '${TeamName}-shopper-deployment-bucket'

  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref S3Bucket
      PolicyDocument:
        Statement:
          - Sid: "AllowSSLRequestsOnly"
            Action: "s3:*"
            Principal: "*"
            Effect: "Deny" # Block if...
            Resource:
              - !Sub "arn:aws:s3:::${TeamName}-shopper-deployment-bucket"
              - !Sub "arn:aws:s3:::${TeamName}-shopper-deployment-bucket/*"
            Condition:
              Bool:
                aws:SecureTransport: "false" # ...the request is not HTTPS
```

Breakdown:

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description:
```

The standard template version (_the only version_), and a descriptive sentence or two.

```yaml
Parameters:
  TeamName:
    Type: String
    Description: # omitted
    Default: rory-gilmore
```

This is the `TeamName` parameter which is required elsewhere in the template. The template will fail without this parameter, so a default value is provided (_rory-gilmore_), but in our Bash script we use the `parameter-override` option in our `aws cloudformation deploy...` command to pass our own values in.

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${TeamName}-shopper-deployment-bucket'
      PublicAccessBlockConfiguration: # do not allow any public access
        BlockPublicAcls: True
        BlockPublicPolicy: True
        IgnorePublicAcls: True
        RestrictPublicBuckets: True
      Tags:
        - Key: Name
          Value: !Sub '${TeamName}-shopper-deployment-bucket'
```

Our first resource, in the `Resources` block, is an S3 bucket. The `Type` is the identifier for a resource to deploy, defined in the [cloudformation resource reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-template-resource-type-ref.html) page.

Next are the properties we need for the bucket, we need to:

- Provide a `BucketName`, in this case a string with our TeamName parameter substituted (`!Sub`) in
  - Remember, bucket names must be globally unique
- Block all of the public access options
- Add a tag to the bucket, which is a metadata key-value pair
  - Tags act as labels for our resources, we can add any tags we want, typical ones include the department that the resource belongs to, the cost center, the project, and so on.

```yaml
  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref S3Bucket
      PolicyDocument:
        Statement:
          - Sid: "AllowSSLRequestsOnly"
            Action: "s3:*"
            Principal: "*"
            Effect: "Deny" # Block if...
            Resource:
              - !Sub "arn:aws:s3:::${TeamName}-shopper-deployment-bucket"
              - !Sub "arn:aws:s3:::${TeamName}-shopper-deployment-bucket/*"
            Condition:
              Bool:
                aws:SecureTransport: "false" # ...the request is not HTTPS
```

This template only contains two Resources, the bucket, and this policy which is attached to it.

Again we need to define the `Type`, and of course a policy requires different properties to a bucket.

- `Bucket`: the bucket the policy should apply to, in this case the one we created above.

The `PolicyDocument` > `Statement` block defines our policy:

- `Sid`: Statement ID, an easily readable label
  - `AllowSSLRequestsOnly`: since all public traffic is blocked, this policy is defining the type of traffic to _allow_
- `Action`: In this case all actions against the S3 service e.g. GetObject, ListBucket, etc.
- `Principal`: the IAM entities the policy applies to, in this case any user/group/role
- `Effect`: the effect of the policy, in this case the policy denies access
  - This can be a little confusing, because we're using DENY in a policy intended to permit access. The logic is that we want to DENY access to everything, except the buckets we make an exception for
- `Resources`: the resource(s) to which we're adding an exception to our DENY effect
  - We've included both the bucket name to cover bucket-level operations, and one ending `/*` to encompass operations against objects in the bucket.
- `Condition`: this lets us state a condition under which the policy applies, in this case based on a `Bool` (Boolean) test
- `aws:SecureTransport`: this is a _global condition key_ which is a boolean statement, returning false if a connection request is using HTTP, and true if using HTTPS

The overall effect of the policy is to:

_Deny all S3 operations, except those to the specified resources, which are using HTTPS._

Despite the tricky syntax and policy logic, this is a relatively simple deployment of a single S3 bucket, and a permissions policy.

The next one is more complex.

---

__etl-stack.yml__:

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  Mystery Shopper ETL pipeline example for AWS week in the Data Engineering Software Academy

Parameters:
  TeamName:
    Type: String
    Description: Enter your team name in format 'team-name' to customise the way your resources are named
    Default: la-vida-mocha
  NetworkStackName:
    Type: String
    Default: project-networking
    Description: Network stack with VPC containing Redshift instance

Resources:
  EtlLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${TeamName}-shopper-etl-lambda'
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
          Value: !Sub '${TeamName}-shopper-etl-lambda'
      Environment:
        Variables:
          SSM_PARAMETER_NAME:
            Fn::Join:
            - '_'
            - Fn::Split:
              - '-'
              - !Sub '${TeamName}_redshift_settings'

  ShopperRawDataBucket:
    Type: AWS::S3::Bucket
    DependsOn:
      - ShopperRawDataBucketPermission
      - EtlLambdaFunction
    Properties:
      BucketName: !Sub '${TeamName}-shopper-raw-data'
      PublicAccessBlockConfiguration: # do not allow any public access
        BlockPublicAcls: True
        BlockPublicPolicy: True
        IgnorePublicAcls: True
        RestrictPublicBuckets: True
      NotificationConfiguration: # trigger the lambda when a file is put in
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Function: !GetAtt EtlLambdaFunction.Arn
      Tags:
        - Key: Name
          Value: !Sub '${TeamName}-shopper-raw-data'

  ShopperRawDataBucketPermission: # allow the bucket to trigger Lambda
    Type: AWS::Lambda::Permission
    Properties:
      Action: lambda:InvokeFunction
      FunctionName: !Ref EtlLambdaFunction
      Principal: s3.amazonaws.com
      SourceArn: !Sub 'arn:aws:s3:::${TeamName}-shopper-raw-data'

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
              - !Sub "arn:aws:s3:::${TeamName}-shopper-raw-data"
              - !Sub "arn:aws:s3:::${TeamName}-shopper-raw-data/*"
            Condition:
              Bool:
                aws:SecureTransport: "false" # ...the request is not HTTPS
```

The first section, containing the template version, description, and TeamName parameter are the same as the previous template, but we also have a NetworkStackName parameter.

```yaml
  ...
  NetworkStackName:
    Type: String
    Default: project-networking
    Description: Network stack with VPC containing Redshift instance
```

This parameter references a stack containing a VPC and associated components which has been deployed for you called `project-networking`.

The `EtlLambdaFunction` resource is quite long so I've split it in two:

```yaml
Resources:
  EtlLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${TeamName}-shopper-etl-lambda'
      Runtime: python3.12
      Handler: mystery_shop_etl_lambda.lambda_handler # file_name.function_name
      Role: !Sub 'arn:aws:iam::${AWS::AccountId}:role/lambda-execution-role' # security rule
      Timeout: 30 # max running time in seconds (make as low as possible)
      ReservedConcurrentExecutions: 10 # how many can run at once
      Code: ./src # use this folder for the zip of lambda code
```

Some of the properties we've already come across, or are very clear with the provided comments; We define a `FunctionName`, and the Python version to be used by Lambda when executing our code is set with `Runtime`.

- `Handler`: this is the function defined in our code which interacts with the Lambda service, typically this is simply called `lambda_handler`
- `Role` refers to the IAM role which grants Lambda the ability to interact with other AWS services.
- `Timeout`, `ReservedConcurrentExecutions`, and `Code` are hopefully clear based on the included comments.

The remaining properties for our Lambda function are about configuring networking and environment variables for our function.

```yaml
      VpcConfig: # use the same networking as RedShift
        SecurityGroupIds:
          - Fn::ImportValue:
              !Sub '${NetworkStackName}-VPCSGID'
        SubnetIds:
          - Fn::ImportValue:
              !Sub '${NetworkStackName}-PrivateSubnet0ID'
      Tags:
        - Key: Name
          Value: !Sub '${TeamName}-shopper-etl-lambda'
      Environment:
        Variables:
          SSM_PARAMETER_NAME:
            Fn::Join:
            - '_'
            - Fn::Split:
              - '-'
              - !Sub '${TeamName}_redshift_settings'
```

- `VpcConfig`: a block defining our VPC (network) configuration
- `SecurityGroupIds` / `SubnetIds`: two required components of the VPC which we need to provide values for
- `Fn::ImportValue`: Imports a value from elsewhere - in this case these values are made available from the `project-networking` stack
- `Environment` / `Variables`: Allows us to create any environment variables required by our Lambda function
  - `SSM_PARAMETER_NAME` This references a parameter in __Systems Manager Parameter Store__ which has been created for you (`Join` and `Split` are used to format the parameter name correctly).
  
>`Systems Manager` is an AWS service which provides a range of very useful an powerful utilities which facilitate easier _management_ of your _systems_.
>
>One feature of Systems Manage is `Parameter Store` which can be used to store values required in your applications and workflows. This is useful for storing credentials so that they don't need to be hard coded or stored on the system. It is also useful for frequently changing values, so that the new value only needs to be changed in one place.
>
>Manage access to your parameters using IAM

The next resource is the `ShopperRawDataBucket` which is where the raw csv data will be uploaded initially.

Many of the statements are the same as those in the deployment bucket, so they've been omitted.

```yaml
  ShopperRawDataBucket:
    ...
    DependsOn:
      - ShopperRawDataBucketPermission
      - EtlLambdaFunction
    Properties:
      ...
      NotificationConfiguration: # trigger the lambda when a file is put in
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Function: !GetAtt EtlLambdaFunction.Arn
      ...
```

- `DependsOn`: tells cloudformation to wait until the specified resources are created before creating this one.
  - Use this when one resource will fail, if it's dependency isn't available
- `LambdaConfigurations`: configure the methods by which our Lambda function will interact with this bucket
- `Event`: the action which will trigger the function
- `Function`: the specific function to call
  - `!GetAtt`: Get Attribute - in this case we want the Amazon Resource Name (ARN) of our Lambda function, which is a unique ID generated during creation of most resources - Note the `EtlLambdaFunction` must be created before we can retrieve the ARN, hence the DependsOn.

```yaml
  ShopperRawDataBucketPermission: # allow the bucket to trigger Lambda
    Type: AWS::Lambda::Permission
    Properties:
      Action: lambda:InvokeFunction
      FunctionName: !Ref EtlLambdaFunction
      Principal: s3.amazonaws.com
      SourceArn: !Sub 'arn:aws:s3:::${TeamName}-shopper-raw-data'
```

The next resource, of `Type: AWS::Lambda::Permission`, allows S3 to trigger the Lambda function.

Hopefully the properties are clear, there is an `Action` to take, the `FunctionName`, the `Principle` requesting the invocation, and the specific `SourceArn` of the bucket.

The final resource in this template is the `ShopperRawDataBucketPolicy`, but this is almost identical to the bucket policy in the `deployment-bucket-stack` at the beginning of this guide, so no need to repeat it.
