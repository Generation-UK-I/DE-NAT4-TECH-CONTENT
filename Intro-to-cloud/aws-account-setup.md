# AWS Account Access

- Open your email client and find the email from `no-reply@login.awsapps.com`
- Click `Accept Invitation`
- Input a **strong** password which matches the ruleset (use a password manager if you can)
- You will then need to register an MFA device with your account. Select the **Authenticator app** option and hit next
- Follow the steps to complete the MFA sign-up stage and click `Assign MFA`
  - You should get a message saying `Authenticator app registered`. Click `Done`
- Once completed, you will be redirected to a new screen. Click on the `AWS Account (1)` box so that it expands, then click on the wider box underneath.
- Click on `Management console` and you will be successfully signed into the AWS console

### Complete the S3 Lab

Use your new account to complete the [S3 CLI Lab](./aws-03-console-s3-exercise.md)

#### Delete everything

Once you have completed the lab...

- Please disable your CloudFront distribution
- Please delete your CloudFront distribution (requires being disabled)
- Please empty and then delete your first bucket
- Please empty and then delete your second bucket
- Please empty and then delete your third bucket