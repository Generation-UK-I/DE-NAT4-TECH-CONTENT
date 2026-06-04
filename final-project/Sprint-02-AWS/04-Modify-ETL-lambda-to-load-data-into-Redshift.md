# Modify ETL lambda to load data into Redshift

## Description

Our choice of data store is going to be AWS [Redshift](https://aws.amazon.com/redshift/). The setup should be nearly identical to what we had in your local PoC (proof of concept).

We need to update the config settings to apply to our Redshift cluster - that is, load the SSM parameter for connections details, and use that to connect to Redshift instead of your local PostgreSQL docker/podman container.

The ETL lambda will need to be setup (i.e. deployed) such that it lives inside the private subnet of the Redshift VPC, so it can talk to the cluster.

## Additional Requirement

- Your local POC (proof of concept) pipeline for a local test file into local postgres must continue to work independently of what is running in AWS,
  - as must your local unit tests
- This is really useful for debugging the sample data files we get in AWS from different branches
- Consider how you will make sure this is always true

## User Story

**As a** business analyst
**I want** to be able to save and access our data in AWS
**So that** I can query it later for analysis

## Acceptance Criteria

- [ ] todo
- [ ] todo
- [ ] todo
