# AWS Account Access

- Open your email client and find the email from `no-reply@login.awsapps.com`
- Click `Accept Invitation`
- Input a **strong** password which matches the ruleset (use a password manager if you can)
- You will then need to register an MFA device with your account. Select the **Authenticator app** option and hit next
- Follow the steps to complete the MFA sign-up stage and click `Assign MFA`
  - You should get a message saying `Authenticator app registered`. Click `Done`
- Once completed, you will be redirected to a new screen. Click on the `AWS Account (1)` box so that it expands, then click on the wider box underneath.
- Click on `Management console` and you will be successfully signed into the AWS console

## AWS CLI

- The way we interact with AWS services through the CLI (Command Line Interface)
- Ease of use over logging in to the console
- If you can do it on the Console, you can do it in the CLI - YAY!
- Simple use-cases: searching logs, quick S3 upload/download

### CLI Installation

Let's install the CLI, so that once we're done we'll be able to communicate with AWS via the command line:

```sh
$ aws <command> <subcommand> [options and parameters]
```

### Installing the CLI - Windows

- Download the [latest version](https://awscli.amazonaws.com/AWSCLIV2.msi)
- Open the download and follow the installation steps
- Verify your installation with the following command:

```sh
C:\> aws --version
aws-cli/2.1.24 Python/3.7.4 Windows/10 botocore/2.0.0
```

### Installing the CLI - MacOS

- Download the [latest version](https://awscli.amazonaws.com/AWSCLIV2.pkg)
- Open the download and follow the installation steps
- Verify your installation with the following commands:

```sh
$ which aws
/usr/local/bin/aws

$ aws --version
aws-cli/2.1.24 Python/3.7.4 Darwin/18.7.0 botocore/2.0.0
```

### Installing the CLI - Linux

Follow the guide which best matches your setup [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html).

### Configuring aws sso

We will use a command called `aws sso` to handle logging into AWS via the CLI.

- On a terminal, run `aws configure sso`
  - If using Linux terminal: run `aws configure sso --use-device-code`
  - Open the provided URL, and enter the code displayed in the terminal.
- When it asks for `SSO session name`, enter a reasonable name, such as `de-course`
- Enter your SSO (_Single Sign-On_) URL (if you don't know it, your instructor will be able to tell you - it will likely be something like `https://<bootcamp-name>.awsapps.com/start#/`)
- Enter the SSO Region, which should be `eu-west-1`
- When it asks for _SSO registration scopes_, hit enter
- For Windows or Mac a webpage will open asking you to sign into the AWS CLI, click the `*Sign in to AWS CLI*` button
- Looking back at your terminal, you will see some text which looks something like this:
   > Using the account ID _xxxxxxxxxxxx_<br />
   > The only role available to you is: StudentAccess <br />
   > Using the role name "StudentAccess"
- When it asks for _CLI default client Region_, enter `eu-west-1`
- When it asks for _CLI default output format_, enter `json`
- When it asks for _CLI profile name_, enter the same name as above e.g. `de-course`
- Check your login works
  - Run `aws sso login --profile <profile-name>` in your terminal (i.e. use the _CLI profile name_ you entered above)

You can now login any time by running `aws sso login --profile <profile-name>` in your terminal.

You can log out of your SSO any time by running `aws sso logout` in your terminal.

## Complete the S3 Lab

Use your new account to complete the [S3 CLI Lab](./aws-03-console-s3-exercise.md)

### After the Lab Delete everything

Once you have completed the lab...

- Please disable your CloudFront distribution
- Please delete your CloudFront distribution (requires being disabled)
- Please empty and then delete your first bucket
- Please empty and then delete your second bucket
- Please empty and then delete your third bucket