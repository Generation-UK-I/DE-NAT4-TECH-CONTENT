# Modify ETL lambda to be called by S3 event

## Description

We need to take the ETL code we wrote for our dockerised application and move it to inside the lambda's handler. We should also know that simply porting it over won't work as we're currently reading data from a local CSV file.

The CSV files will be landing in S3 every evening at 8pm. We need to configure our code so that we can read the CSV from S3. Not only this, but we need to execute our lambda from an event when a new file lands in S3.

You will need:

- s3 bucket trigger, if you don't already have it from the previous story
- s3 bucket permissions for the triggered lambda to access the s3 bucket
- code in your lambda to get the bucket and file name (s3 key) from the event
- log this out
- code to load this file from s3 using boto3
- code to print out something like the number of rows loaded, for example
  - (do not log the whole file contents, this will reveal any PID!)

## Additional Requirement

- Your local POC (proof of concept) pipeline for a local test file into local postgres must continue to work independently of what is running in AWS,
  - as must your local unit tests
- This is really useful for debugging the sample data files we get in AWS from different branches
- Consider how you will make sure this is always true

## Technical info

- You will need to set up a link between your S3 bucket and the Lambda, i.e a Trigger or _Notification_
- In AWS, each individual file being sent to the bucket triggers the lambda _once per file_ with an _event_
  - So only look for the bucket & file listed in the `Records[0]` of the event
  - You do not need code for multiple files (`Records[]` will only have one element)
  - Most importantly, nor do you need to scan the bucket for files you already processed
- The 'event' object sent to our lambda function will contain the _bucket name_ and _file name_ (object key) - so, the _name_ but not the _data_ from the file
- Which will allow our lambda to load the data from the file it's self, according to it's needs

## User Story

**As a** developer
**I want** to invoke my ETL lambda with an S3 event when a file has been uploaded to a bucket
**So that** I can process many data files concurrently

## Acceptance Criteria

- [ ] todo
- [ ] todo
- [ ] todo
