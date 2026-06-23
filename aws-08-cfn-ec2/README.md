# AWS 08 - Intro to EC2 + EC2 with IaC

Here we introduce running virtual servers in EC2, setup and deploy one with Cloud Formation, and configure it to run an application for us (in this case, Grafana).

- For those less familiar with AWS - The slides do cover all the parts of all the CF objects we create - do have a read through in advance!

We use Grafana as it is used for the visualisations in the team project - a fully worked example is in the [data-academy-pipeline-example repo](https://github.com/infinityworks/data-academy-pipeline-example).

## Related documents

> Important! You will find these useful for reference:

- Main [../README.md](../README.md), `Final Project (second half of course)` section
- Main [../README.md](../README.md), `Related Documents` section for
    - Related repos
    - Team project documents!

## Overview

- What is EC2
- Running a virtual server in the cloud
- Configuring the startup of an EC2
- Hosting applications inside our Servers

## AWS sessions list

This is the list of AWS sessions done so far, and the following ones:

- AWS 01 AWS + Cloud Intro ✅ _1.5hrs_
- AWS 02 AWS CLI Setup ✅ _1.5hrs_
- AWS 03 S3 Storage (Console) ✅ _1.5hrs_
- AWS 04 CloudFormation Intro + S3 Storage (IaC) ✅ _1.5hrs_
- AWS 05 Lambda Intro ✅ _1.5hrs_
- AWS 06 Lambda (IaC) ✅ _1.5hrs_
- AWS 07 Redshift (IaC) ✅ _1.5hrs_
- AWS 08 EC2 (IaC) + Grafana setup ⬅ _1.5hrs_
- AWS 09 Queues _1.5hrs_
- AWS 10 Monitoring _1.5hrs_

## Timings

- This session is timetabled for 1 block at 1.5 hrs, i.e. 0.25 elapsed training days

## Assessments

To check the learner progress in this session we have:

- Follow-along exercises to use the AWS CLI with CloudFormation templates
- Emoji Checks to confirm learner understanding and progress

## Prep

- Run through the slides and exercises yourself in advance
- For those less familiar with AWS - The slides do cover all the parts of all the CF objects we create - do have a read through in advance!
- Create the session files (pdf and zip) for distribution using `make generate-session-files f=module_name` or `make gsf-local f=module_name`
- Ensure you can authenticate to AWS using the correct credentials for the course (e.g. School of Tech, Generation, Client, etc.)

## Session

- Have AWS console and CLI ready to use
- Run the slide deck
- Demo the IaC yourself, show it working
- Run the exercises as breakouts, code-along(s) or live-shares as you see fit

---

### Tips for the team projects (offline)

> For the team projects, there is a file of a few pointers and gotchas to consider.

- See [./handouts/README-team-project-considerations.md](./handouts/README-team-project-considerations.md)
