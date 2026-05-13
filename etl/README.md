# ETL

This module builds on the content from `databases` with the addition of grouping, aggregating and renaming columns and their contents (e.g. `GROUP BY` , `COUNT`, `AVERAGE`, `SUM` and `AS`)

## Overview

- High level definition of ETL
- What problems can ETL solve?
- What happens in each stage?
- ETL vs ELT

## Timings

- This session is timetabled for 2 blocks at 1.5 hrs each, i.e. 0.5 elapsed training days
- The formative assessments occur during this and are included in that timing
- The exercises for this session (done in breakouts) are also included in that time

## Assessments

To check the learner progress in this session we have:

- Multiple Quizzes throughout the session with answer walkthrough
- Follow along demo for the students
- Set of exercises are ran in breakout room

## Prep

- Create the session files (pdf and zip) using `make generate-session-files f=module_name`
- Review the slides and exercises
- Familiarise yourself with the above SQL commands and also the use cases for an ETL pipeline
Be ready to demonstrate working code for each of the 'Demo' sections

Needs Docker or Podman running a postgres container that we can use to save the data - see also the [Docker](../docker/) or [databases](../databases/) or [databases-sot](../databases-sot/) sessions.

- The [docker-compose.yml](./handouts/docker-compose.yml) used here is the same as for the above mentioned [databases](../databases/) session.

## Session

- Run the presentation

### Exercises in the Session

The exercise asks learners to write a Python script that executes an ETL pipeline.

Needs Docker running - see also the Docker session. We need an Adminer and MySql container for the exercise code to save the data in.
