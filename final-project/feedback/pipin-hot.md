# ETL Project Feedback

## Team: Pipin' Hot

### Team Members: Ric, Mukarram, Marcell, Zak

Pipin' Hot delivered a balanced presentation that demonstrated sound technical decision-making and clear evidence of iterative development.

#### Project Overview and Delivery

__Mukarram__ began by outlining the client's key business challenge: data was isolated across multiple branches, making it difficult to identify trends and generate meaningful insights at an organisational level.

__Ric__ explained the proposed solution, project scope, and MoSCoW prioritisation process. The team adopted Agile practices with rotating responsibilities, regular Product Owner engagement, and flexible task allocation based on both existing strengths and learning objectives.

__Marcell__ described the team's development process, beginning with a local proof of concept before migrating the solution into AWS. CloudFormation was used for infrastructure deployment, helping introduce consistency and repeatability.

The ETL flow consisted of:

- CSV Upload → Amazon S3 → AWS Lambda (Extract, Transform, Load) → Amazon Redshift
- CloudWatch logs were used to demonstrate successful execution.

__Marcell__ also discussed ongoing work to improve data quality, noting that date and time fields still required additional transformation. The team had begun data normalisation work by separating the dataset into three related tables to reduce redundancy.

#### Reflections and Learning

__Zak__ reflected honestly on the team's development journey. Achieving a fully functioning solution took longer than expected, with significant progress occurring towards the end of Sprint 2. Amazon Redshift introduced challenges, particularly relating to UUID data type compatibility and troubleshooting.

The team intentionally deprioritised Grafana and SQS to maintain focus on completing the MVP, reflecting sensible prioritisation and scope management.

Interestingly, once the proof of concept was complete, migration into AWS proved more straightforward than anticipated.

#### Q&A Discussion

When asked what they would change if starting again:

- __Marcell__ suggested separating functionality into multiple Lambda functions.
- __Zak__ proposed revisiting and improving the database schema design.

In response to questions regarding PII protection:

- __Zak__ discussed encryption and secure transport through HTTPS.
- __Marcell__ explained that sensitive fields are removed during transformation and that services operate within the same VPC as Redshift.
- __Ric__ highlighted the implementation of AWS multi-factor authentication.

When discussing project achievements:

- __Ric__ was particularly proud of successfully migrating a local proof of concept into a cloud-hosted solution, describing the journey from a local experiment to a production-style implementation.
- __Zak__ highlighted his increased understanding of AWS technologies.
- __Marcell__ emphasised his growing knowledge of AWS service integration.

#### General Observations

The team demonstrated sensible prioritisation, realistic reflections, and a strong appreciation for the challenges of cloud migration. Their decision-making consistently reflected delivery of business value over implementation of lower-priority features.
