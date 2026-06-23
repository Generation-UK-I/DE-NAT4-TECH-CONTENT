# AWS 08 - EC2 and Grafana with CloudFormation

> This exercise is done as a code-along with the whole class during the session.
>
> The summary steps are re-created here.

## Stack template

We need to start from the partially complete file [../handouts/etl-stack.yml](../handouts/etl-stack.yml)

For further details refer to the slides and solutions folder (deliberately not duplicated here):

- Add CF Parameters for
    - `EC2InstanceProfileRoleName`
    - `EC2InstanceIngressIp`
    - `EC2UserData`
- Add a `GrafanaEc2Instance` resource with the right type and properties

## Deployment

### Step 01.A - Log into AWS

- Open a terminal in the [handouts](../handouts/) folder
    - If using Windows this can be in Powershell
- Log in depending on your AWS login method
- Run
    - Either `aws sso login --profile <your-profile-name>`
    - or `aws-azure-login --profile <you-profile-name>`
    - or use your alias

### Step 01.B Deploy

- Make sure your terminal is in the [handouts](../handouts/) folder
    - If using Windows this can be in Powershell
- Find your laptops public IP address from e.g. <https://whatsmyip.org>
- Run the relevant `./deploy.[sh|ps1]` script like as below
    - Your user-name must be entered like `lowercase-with-dashes` as it will be used in the S3 Bucket names as well
    - Your team-name must be entered like `lowercase-with-dashes` as it will be used to lookup your redshift connection details in Parameter Store

```sh
cd handouts # only if not already in that folder

./deploy.[sh|ps1] <aws_profile> <your-name> <team-name> <your-ip>
# e.g run one of these:
# MacOS / WSLv2 / GitBash
./deploy.sh sot-academy rory-gilmore la-vida-mocha 12.34.56.78
# Windows Powershell
./deploy.ps1 sot-academy rory-gilmore la-vida-mocha 12.34.56.78
```

- Wait until the script has finished updating the stack

## Deployment Validation

- Open the AWS (web) console and check the deployment
    - Check the CloudFormation events on your Stack

## Grafana

Follow the steps in the slides to

- Log into Grafana
- Connect Grafana to Redshift
- Add settings for a data source
- Test the data source
- Add a visualisation

All done!
