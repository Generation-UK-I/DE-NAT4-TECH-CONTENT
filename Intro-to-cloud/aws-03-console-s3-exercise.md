# AWS 03 - Storage in S3

S3 has a wide range of features, it isn't _just_ for storing objects.

## Part 1 - Dealing with files

Use the AWS CLI in your terminal to perform the following actions. You will need to look up the commands (see below). if you get stuck, sample commands to use are in the `aws/solutions` folder.

NB: Unless AWS_PROFILE is already set in your environment, make sure to put `--profile your-profile-name` at the end of every command to specify your personal profile.

### Part 1.A Log into AWS

- Open a terminal in the [handouts](../handouts/) folder
    - If using Windows this can be in Powershell
- Log in depending on your AWS login method
- Run
    - Either `aws sso login --profile <your-profile-name>`
    - or `aws-azure-login --profile <you-profile-name>`
    - or use your alias

### Part 1.B Use AWS CLI

1. Using the CLI, create two S3 buckets
    1. Bucket names must be only using `a-z` (lowercase), `0-9` or `-`!!
    1. Use a name like `your-name-cohort-name`
    1. Bucket names are **globally** unique, so if someone in the world already created a bucket called `your-name-test-123`, you will not be able to use it
1. Upload the files in the `handouts` folder your first bucket
    (make sure there is no personal information in them)
1. _List_ your buckets
1. _List_ the files in your first bucket
1. _Copy_ a file from the first to second bucket
1. _Move_ a file from the first to second bucket
1. _Delete_ a file from either bucket

Hint: Here is a link to the [S3 CLI docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html) - us these to work out the commands you need.

## Part 2 - Setup a website in S3

In this exercise we will be leveraging S3 in a slightly more unusual way. S3 is a fantastic tool for hosting static websites. On a static website, individual webpages include static content. They might also contain client-side scripts.

A lot of websites are becoming static websites which means they run zero server side code and consist of only HTML, CSS and JavaScript. With no server side code to run, there is no reason to host them on a traditional server.

By using the static website hosting feature on an S3 bucket, we can host static websites for one to two dollars a month and scale to handle millions of users. So let's try it out!

### Setting up the bucket

1. Navigate to the S3 console and click `Create bucket`
1. Enter a name for the bucket (bucket names are globally unique, so if someone has taken your name, tough!)
1. Set the `AWS Region` to `eu-west-1`
1. Scroll to the bottom and hit `Create bucket` again
1. Open up the created bucket
1. Navigate to `Permissions --> Block public access (bucket settings) --> Edit`
1. Ensure all checkboxes next to and below `Block all public access` are ticked (they should be by default)
1. Now we need to upload `index.html` to our bucket. This file will have been provided to you. On the `Objects` tab of your bucket, select `Upload`
1. Drag and drop the file onto the screen to upload it

### Setting up a CloudFront distribution

CloudFront is AWS's content delivery network (CDN) that caches and delivers web content from edge locations worldwide, reducing latency and improving load times for users. It optimises content delivery by serving cached copies of your website's assets from the nearest edge location to users, ensuring fast and reliable performance.

Because we have securely set up our bucket to block public access, we need to configure a CloudFront distribution so we can access bucket contents via HTTPS.

1. Navigate to the CloudFront service homepage in the AWS Console
1. Click the `Create Distribution` button
1. Under `Origin domain` select the `<bucket-name>.s3.amazonaws.com` URL for the bucket you just created and enter a name for it under `Name`, e.g. `Your-name origin domain`
1. Under `Origin access` select `Legacy access identities`, click the `Create new OAI` button, and enter a name for it, e.g. `Your-Name OAI`
1. Ensure you select your newly created OAI under `Origin access`
1. Under `Bucket policy` select `Yes, update the bucket policy`
1. Under `Default cache behavior`, select:
    1. Viewer protocol policy -> HTTPS only
    1. Cache key and origin requests -> Legacy cache settings
    1. Leave everything else the same
1. Under `WAF` select `Do not enable security protections`
1. Under `Settings > Supported HTTP versions` also tick `HTTP/3`
1. Under `Default root object`, enter `index.html`
1. Enter a description at the bottom
    1. Please put your name in it e.g. `Your-Name: front for bucket files`
1. Finally, click `Create distribution`

Once your CloudFront distribution changes out of `Deploying` state, it's ready!

Everything should be set up at this point, so:

- Navigate to the `General` tab of the distribution you made,
    - then copy the `Distribution domain name` URL
- Open the URL in a new browser window and voila...
    - your index.html file should be getting served and cached over HTTPS!

## Part 3 - Delete everything

- Please _disable_ your CloudFront distribution
- Please _delete_ your CloudFront distribution
- Please _delete_ your first bucket
- Please _delete_ your second bucket
- Please _delete_ your third bucket
