# Create SQS queue to connect each lambda to the next

## Description

When separating the ETL lambda into two or more pieces, we will need a queue between each of them.

## User Story

**As a** developer
**I want** to create a queue that sits between each of my lambdas
**So that** I can decouple my workload with a mature architecture

## Design

For example, if you have an initial Extract & Transform lambda woken up by the file landing in S3, you will need one queue for it to send data to, that in turn wakes up the Load Lambda (that saves data to your redshift DB).

If you have 3 Lambdas (E, T, L) would need 2 queues, one between the E-T lambdas, and one between the T-L lambdas.

## Technical notes

- Lambdas don't communicate well directly (networking issues often arise, they can be blocking, else you have to do async handling).
- When you separate lambdas, they need another way to communicate
- Typically you either:
  - Add a queue between them (e.g. SQS, SNS). Lambda1 sends a json message with some data to the queue, which in turn wakes up Lambda2 with the message
- Or
  - Lambda1 saves it's output in a different S3 bucket / folder, and a trigger on that wakes up Lambda2 with the filename

## Acceptance Criteria

- [ ] todo
- [ ] todo
- [ ] todo
