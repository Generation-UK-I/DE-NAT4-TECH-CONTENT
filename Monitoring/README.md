# Monitoring

This module introduces learners to the key components of monitoring.

Related sessions cover:

- [AWS intro + services](../aws/README.md)
- [DevOps inc. CI](../devops/README.md)
- [Cloudformation inc. CD](../cloudformation/README.md)
- [Data Warehousing inc. mention of Redshift](../data-warehousing/README.md)
- [Monitoring](../monitoring/README.md)
- [Queues inc SQS](../queues/README.md)
- [Data Streams inc Kinesis](../data-streams/README.md)

## Overview

- What does software monitoring consist of?
- Why do we monitor software?
- Monitoring infrastructure
- Monitoring applications

### AWS sessions list

This is the list of AWS sessions done so far, and the following ones:

- AWS 01 AWS + Cloud Intro ✅ _1.5hrs_
- AWS 02 AWS CLI Setup ✅ _1.5hrs_
- AWS 03 S3 Storage (Console) ✅ _1.5hrs_
- AWS 04 CloudFormation Intro + S3 Storage (IaC) ✅ _1.5hrs_
- AWS 05 Lambda Intro ✅ _1.5hrs_
- AWS 06 Lambda (IaC) ✅ _1.5hrs_
- AWS 07 Redshift (IaC) ✅ _1.5hrs_
- AWS 08 EC2 (IaC) + Grafana setup ✅ _1.5hrs_
- AWS 09 Queues ✅ _1.5hrs_
- AWS 10 Monitoring ⬅ _1.5hrs_

## Timings

- This session is timetabled for 3 blocks at 1.5 hrs each, i.e. 0.5 elapsed training days
    - The big 30m exercise for CloudWatch needs to start about 1.5hrs in at the latest
    - Then you will have time for that, the Grafana intro, and the 30m Grafana exercise
- The formative assessments occur during this and are included in that timing
- The exercises for this session (done in breakouts) are also included in that time

## Assessments

To check the learner progress in this session we have:

- Emoji checks on each topic
- Extensive exercises on:
    - Uploading a lambda and invoking it
    - Analysing the logs in CloudWatch
    - Using CloudWatch Insights
    - Running Grafana locally
    - Setting up Grafana data sources
    - Setting us Grafana dashboards

## Prep

It helps in advance to get everyone pulling grafana, plus stopping and removing any old containers to avoid port clashes:

```sh
docker pull docker.io/grafana/grafana
docker ps -a
docker stop <container-id>
docker rm <container-id>
```

- Create the session files (pdf and zip) using `make generate-session-files f=module_name`
- Review the slides and exercises
- The exercises are extensive and take about an hour each

### Prep - Exercises

Please distribute [monitoring-exercises.md](./exercises/monitoring-exercises.md) for Generation, and [monitoring-exercises-sot.md](./exercises/monitoring-exercises.md) for School of Tech.

### Prep - Final Project section

The "Final Project" section in [monitoring-exercises.md](./exercises/monitoring-exercises.md) section links to two files:

- [final-project-grafana-setup.md](./exercises/final-project-grafana-setup.md) for Generation
- [final-project-grafana-setup-sot.md](./exercises/final-project-grafana-setup-sot.md) for School of Tech

These tell the teams how to set up grafana for themselves in an AWS EC2 later, have a read through so you are familiar. There are currently two versions as School of Tech has migrated to a new version of AWS week, while Generation haven't yet but will soon.

TODO: Update Generation material to reference new version of grafana setup when migration has occurred.

### Prep - required roles

Make sure you have run the commands for the AWS and project setup in advance:

- The instructions are here: [repo data-academy-final-project-infrastructure#commands-to-deploy](https://github.com/infinityworks/data-academy-final-project-infrastructure#commands-to-deploy)
- This creates the roles that you and the learners will need in this session and/or the next few weeks:
    - `lambda-execution-role`(for Generation)
    - `de-academy-ec2-role` (re-used for the team project ec2 to run Grafana)
        - also the `de-academy-ec2-role-instance-profile`
    - `github-cicd-role`
    - `ScopePermissions` policy for use as a Permissions Boundary

## Session

- Run the slide deck
- Give the learners some time to set up the Podman/Docker instance for Grafana
- Exercises
    - The big 30m exercise for CloudWatch needs to start about 1.5hrs in at the latest
    - Then you will have time for that, the Grafana intro, and the 30m Grafana exercise
- Try and get all learners by the end of the lesson to have loaded up the Grafana dashboard and been able to create a new dashboard and panels
- When you get to the `Offline task - Final Project Grafana` section,
    - Generation
        - Point out that the "Final Project" section in [monitoring-exercises.md](./exercises/monitoring-exercises.md) section, and the file it links to [final-project-grafana-setup.md](./exercises/final-project-grafana-setup.md) are for team project time
    - School of Tech
        - Point out that the "Final Project SoT" section in [monitoring-exercises-sot.md](./exercises/monitoring-exercises-sot.md) section, and the file it links to [final-project-grafana-setup-sot.md](./exercises/final-project-grafana-setup-sot.md) are for team project time
