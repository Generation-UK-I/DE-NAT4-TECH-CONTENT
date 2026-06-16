# Example script for deploying the Monitoring Lambda
# All of <your-name>, <aws-acct-id> and <profile-name> need replacing

aws lambda create-function --function-name '<your-name>-cafe-monitoring' `
    --zip-file 'fileb://monitoring_lambda.zip' `
    --handler 'lambda_function.lambda_handler' --runtime 'python3.12' `
    --role 'arn:aws:iam::<aws-acct-id>:role/lambda-execution-role' `
    --profile '<profile-name>' --region 'eu-west-1' --timeout 60
