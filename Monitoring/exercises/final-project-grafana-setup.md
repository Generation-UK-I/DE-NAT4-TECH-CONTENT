# Final Project - EC2 Launch Docker/Grafana on Startup & Save Changes

Each team will need to make a Virtual Machine (EC2) in AWS with CloudFormation - you will then set it up to run docker for you, and docker to run the Grafana image.

Read this whole file all the way through before starting any of the steps!

## EC2 Setup

For setting up an AWS Virtual Machine (EC2) running Grafana, you should follow the same steps as demonstrated in `aws-08-cfn-ec2`.

**Important** - _Nominate one person in your project team to do the setup - they will end up with the SSH key._

You can connect to your EC2 via SSH by clicking the `Connect` button on the top right of the EC2 instance screen in the AWS Console. From here you can copy the `ssh` command at the bottom of the screen to run it in your terminal.

## Grafana setup

- Browse to it by going to the Instance's public IP address (check the EC2 page)
    - e.g <http://12.34.56.78:80> (use your IP address)
- Log into Grafana with user `admin` and password `admin`
- Change the admin password to a _secure_ one, and put it in your password manager.

### Setup Grafana users

To create a new user login for each team member, navigate to `Server Admin --> Users --> New user` and begin creating unique users with _secure passwords_.

Put these in your password manager.

### Connecting Grafana to CloudWatch

Just like in the earlier exercise, we need to connect a data source in order to generate some graphs and metrics.

1. In Grafana, navigate to `Configuration -> Data Sources`. Select `Add data source`, search for `CloudWatch` and select.
1. Give it a name, or leave as default.
1. Leave other settings as default.
1. Set region to `eu-west-1`.
1. Select `Save & Test`. You should see a confirmation `Data source is working`.

### Creating a Lambda metric

We can make graphs and metrics for our Lambda - e.g. how many time it ran, how long it took, how many errors there were.

1. Create a new dashboard and add a new panel.
1. Select `CloudWatch` as the query type, and `CloudWatch Metrics` as the query mode.
1. Select `AWS Lambda` as the namespace, and `Invocations` as the metric name.
1. Add a new Dimension. Select `Function name` as the resource and select the dimension value as your teams ETL lambda.
1. Update the time query to be last 24 hours or 2/7 days if you need to go back that far to see data being graphed.

You should be able to now see how many times your lambda has been invoked over the time elapsed configured for the time period. You can also choose different metric options to suit your needs. For example, you can select `Error` and `Duration` as the metric name, as well as different stats such as `Average`, `Sum`, `Min` and `Max`.

As team, think about what kind of monitoring metrics you can establish to display on your new dashboard.

### Connecting Grafana to Redshift

For the Grafana instance deployed on EC2, in the user interface:

- Install the "Amazon Redshift" plugin
- Add a "Redshift" datasource
- Leave the _assumed role_ blank (as it defaults to the role on EC2 instance)
- Set default region to `eu-west-1`
- Select the redshift cluster in "Cluster Identifier"
- Add your team's database user and database name (these credentials can be found in AWS SSM Parameter Store)

You can now create dashboards by using the data from your Redshift database, using SQL.

As a team think about what data from Redshift you want to display, for example, revenue per day or week, number of items sold per day, number of each type of drink sold in the last week, and so on. You wil have to create the SQL for this yourselves.

# Final Project - EC2 Launch Docker/Grafana on Startup & Save Changes

Each team will need to make a Virtual Machine (EC2) in AWS - you will then set it up to run docker for you, and docker to run the Grafana image.

Read this whole file all the way through before starting any of the steps!

## EC2 Setup

For setting up an AWS Virtual Machine (EC2) running Grafana, you should follow the same steps as in the AWS EC2 exercise.

**Important** - _Nominate one person to do the setup - they will end up with the SSH key._

### Security group for your EC2

Make a new team security group as per `aws/exercises/aws-exercises.md` -> `### Security Group Setup` section.

_BUT_ - When making the security group, do this:

1. Use your team name e.g. `your-team-sg`
1. Limit all Inbound access to your teams IP addresses only
    1. For each person in your team:
        1. Select `SSH` for `Type` and `My IP` for `Source` (to make a rule for port 22)
        1. Select `HTTP` for `Type` and `My IP` for `Source` (to make a rule for port 80)

### Your EC2

Make a new team EC2 as per `aws/exercises/aws-exercises.md` -> `### EC2 Instance Setup` section.

1. Use the most recent AWS "Amazon Linux 2023" machine image (AMI)
1. SSH into the instance with the SSH key you downloaded. DO NOT LOSE THIS KEY!
    1. **DO NOT** put this in any Git folder - this would be like adding a password to git, but worse, which is **VERY BAD**
1. Then to install docker inside it you need to run this:
    if on Linux / Mac, run these sudo commands. If on Windows, run the terminal as administrator, then run the same commands without `sudo`

    ```sh
    sudo yum install docker -y
    sudo service docker start
    sudo usermod -a -G docker ec2-user
    sudo chkconfig docker on
    ```

---

## Docker Setup

The following steps are to ensure any changes you've made in Grafana are saved when you Stop/Pause your instance and Start it again.

- Connect/SSH into your EC2 Instance.
- Ensure your Grafana Docker Image is **_not_** running. To check this, run the command:
    - `docker ps -a`
- If it is running, use this to stop it and remove it:
    - `docker stop <container-id>`
    - `docker rm <container-id>`
- Create a docker volume by running the following command:
    - `docker volume create grafana-storage`
- Verify the docker volume has been created by running command:
    - `docker volume ls`
- Verify you can run your Grafana image/container with volume by running this command:

    ```sh
    sudo docker run -d -p 80:3000 --rm \
        --volume grafana-storage:/var/lib/grafana docker.io/grafana/grafana ;
    ```

- Check the container is running with `docker ps -a`
- Also check the Grafana site is running by going to the Instance's public IP address (check the EC2 page)
    - e.g <http://12.34.56.78:80> (use your IP address)
    - You don't log in yet (See steps later for that)
- Now go to AWS and click `Stop Instance` to stop the instance
- From the EC2 Instance list, select your instance and click the `Actions` drop-down -> `Instance settings` -> `Edit user data`
- In the `Edit user data` page, ensure `Modify user data as text` is selected and then copy & paste the following into the text field:

```yaml
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/sh
sudo docker run -d -p 80:3000 --rm --volume grafana-storage:/var/lib/grafana docker.io/grafana/grafana
--//--
```

- Click `Save`
- Start your Instance again
- Docker should now be running automatically
- Verify this by logging back in and running `docker ps -a`
- Also verify it by browsing to the Grafana site via the Instance's public IP address, and check the changes you made are there, e.g <http://12.34.56.78:80>
    - You don't need to log into it yet

---

## Grafana setup

- Browse to it by going to the Instance's public IP address (check the EC2 page)
    - e.g <http://12.34.56.78:80> (use your IP address)
- Log into Grafana with user `admin` and password `admin`
- Change the admin password to a _secure_ one, and put it on your teams _private_ Slack or MS Teams channel

### Setup Grafana users

To create a new user login for each team member, navigate to `Server Admin --> Users --> New user` and begin creating unique users with _secure passwords_.

### Connecting Grafana to CloudWatch

Just like in the earlier exercise, we need to connect a data source in order to generate some graphs and metrics.

1. In Grafana, navigate to `Configuration --> Data Sources`. Select `Add data source`, search for `CloudWatch` and select.
1. Give it a name, or leave as default.
1. Leave other settings as default.
1. Set region to `eu-west-1`.
1. Select `Save & Test`. You should see a confirmation `Data source is working`.

### Creating a Lambda metric

We can make graphs and metrics for our Lambda - e.g. how many time it ran, how long it took, how many errors there were.

1. Create a new dashboard and add a new panel.
1. Select `CloudWatch` as the query type, and `CloudWatch Metrics` as the query mode.
1. Select `AWS Lambda` as the namespace, and `Invocations` as the metric name.
1. Add a new Dimension. Select `Function name` as the resource and select the dimension value as your teams ETL lambda.
1. Update the time query to be last 24 hours or 2/7 days if you need to go back that far to see data being graphed.

You should be able to now see how many times your lambda has been invoked over the time elapsed configured for the time period. You can also choose different metric options to suit your needs. For example, you can select `Error` and `Duration` as the metric name, as well as different stats such as `Average`, `Sum`, `Min` and `Max`.

As team, think about what kind of monitoring metrics you can establish to display on your new dashboard.

### Connecting Grafana to Redshift

> We will use the PostgreSQL data source as it is (a) similar to the library we are using in our lambda code and (b) the official RedShift data source has proven "extremely unreliable".
>
> The settings you need are in your RedShift _parameter_ in AWS, e.g `la_vida_mocha_redshift_settings`

- In the AWS web console, open up Parameter Store in Systems manger and find your connection details

### Connecting Grafana to Redshift

- Using the menu navigate to `Connections / Data sources`
- Search for `Postgres` (it should be pre-installed)
- Click it to add a new data source

![](./img/postgres-datasource-search.png)

### Task - Settings for data source

- Enter the host in format `server:port` e.g. `redshiftcluster.~~~.com:5439`
- Enter the DB name e.g. `la_vida_mocha_cafe_db`
- Enter the DB user e.g. `la_vida_mocha_user`
- Enter the DB password e.g. `abcdefghijk`

![](./img/postgres-datasource-connection-info.png)

### Task - Test data source

- Scroll to the bottom of the datasource window
- Click "Save & Test"
- A green success flash should appear

![](./img/postgres-datasource-save-test.png)

### Next Steps

Make a new dashboard and think about what could go on it.

As a team think about what data from Redshift you want to display, for example, revenue per day or week, number of items sold per day, number of each type of drink sold in the last week, and so on. You will have to create the SQL for this yourselves.
