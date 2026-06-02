# Code along - creating a lambda

Lets have a look at how to make a Python Lambda from scratch.

## Creating a lambda

- Find the `Lambda` service
- Ensure you are in the correct region `eu-west-1`
- Click on "Create Function"
- Select "Author from scratch"
- Enter a function name e.g. `your-name-de-demo-lambda`
- Select the most recent Python Runtime version you can
  - Notice anything about the available versions?

Available Python runtimes in AWS lag behind the most recent releases - it takes AWS time to set them up and test them after Python.org release them. This is the same for all supported Lambda Runtimes (Node, Java, etc).

Adding a Tag called Name makes lots of the AWS (web) Console show us the logical name, which by default, lots of it does not!

- Under `Change default execution role`, select `Use an existing role` and enter `lambda-execution-role`
- Create the function
- Once the function is created, go to the `Configuration` tab and select `Tags` at the side
- Add a new tag with key `Name` and value of the function name

### Events

Lets have a look at how Events work and logging them.

- Make a new test event with the `Hello-World` template
- Save it for later
- Trigger the Lambda with your test event
- Check the logs in the Lambda page
- Click through to the logs in CloudWatch

A test event in Lambda is a sample input payload used to manually invoke a Lambda function in the AWS Console (typically for testing purposes). It allows you to simulate how your Lambda function would behave when triggered by an actual event source e.g. S3

To create a test event:

- From the Lambda function, go to the "Test" tab
- Enter an event name
- Click 'Save' to save the event
- Click 'Test' to test the event

Lets log our `event` object.

- Add code to Log (`print()`) the event object
- (Re)deploy the lambda
- Trigger the lambda with your saved Test Event
- Check the CloudWatch logs now have more in them

**Note**: Always (re)deploy lambda functions when code is updated or changes won't be reflected !

## Configuration with env vars

Lets have a look at how Environment Variables ("env vars") work.

- **Never** use these for passwords!
- Add an env var e.g. `FAVOURITE_MOVIE` with a suitable value
- Add code to import `os`
- Add code to put the env var in a variable
  - e.g. `fave_movie = os.environ['FAVOURITE_MOVIE']`
- Add code to print the variable
- (Re)deploy the lambda
- Re-Test the lambda and recheck the logs

Using an `.env` file will NOT work. To set a environment variable:

- From the lambda function go to 'Configuration' tab
- Select 'Environment variables' on the left hand side
- Click 'Edit' to add a new one

### Updating the return value

The return value of a Lambda is used to indicate success/failure to the caller, and convey extra information.

- Demo making a basic Hello message JSON for the return value
- (Re)Deploy the lambda
- Re-Test the lambda
- Check the return value in the logs

Update your lambda return value to say Hello to yourself

- Repeat what the Instructor just showed you
- (Re)Deploy the lambda
- Re-Test the lambda
- Check the return value in the logs

---

### Sample handler code

A sample of what our code might now look at is in the [./handouts/sample_python_lambda.py](./handouts/sample_python_lambda.py) file.
