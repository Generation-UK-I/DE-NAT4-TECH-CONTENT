# Move Extract + Transform steps to own lambdas

## Description

Put the Extract and / or Transform steps in their own lambda(s) with added queues between as required.

## User Story

**As a** developer
**I want** to move the 'extract' stage of the ETL pipeline to its own lambda
**So that** I can decouple my architecture

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
