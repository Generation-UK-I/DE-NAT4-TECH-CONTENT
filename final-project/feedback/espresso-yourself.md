# ETL Project Feedback

## Team: Espresso Yourself

### Team Members: Ishak, Suzanne, Ted, Yousaf

Espresso Yourself delivered a polished and business-focused presentation that clearly articulated both the client's problem and the value of the proposed solution.

#### Project Overview and Delivery

__Ishak__ introduced the team and explained their decision to adopt Agile ways of working with rotating team roles. This approach allowed each member to gain experience across multiple responsibilities. He established a strong narrative by explaining how the client was currently reliant on manual processes and required an automated pipeline to move data efficiently from retail stores into a reporting environment.

__Suzanne__ described the team's planning methodology, including the use of MoSCoW prioritisation to define a realistic MVP within the available timeframe. The team maintained a strong client-centric focus throughout the project. Their key requirements included:

__Must Have__:

- CSV upload to Amazon S3.
- Lambda-triggered processing.
- Loading transformed data into a local or cloud-based database.

__Could Have__:

- Grafana dashboards and visualisations.

__Won't Have__:

- SQS implementation within the MVP.

She also outlined the team's Agile processes, including stand-ups, retrospectives, product owner meetings, Jira ticket management, and GitHub branching strategies. Team roles were allocated based upon individual strengths and previous successes.

__Ted__ demonstrated evidence of successful pipeline execution through CloudWatch logs. Due to external issues with Redshift credentials, the team relied on screenshots rather than a fully live demonstration. He also reviewed Python code responsible for data cleansing and PII removal before showing examples of the cleaned dataset.

__Yousaf__ then explained the technical architecture and the flow of data through the ETL stages:

- CSV (Raw Data) → S3 → Lambda → Redshift

#### Reflections and Learning

__Ted__ highlighted the team's successful completion of Sprint 2 objectives and praised the strong collaboration demonstrated throughout the project. He acknowledged that adapting to a cloud-first environment was initially challenging.

The team also identified AWS services, CloudFormation, and Lambda development as significant learning areas requiring additional troubleshooting and experimentation.

#### Future Improvements

The team proposed several logical next steps:

- Full migration to Redshift.
- Decoupling components using Amazon SQS.
- Building Grafana dashboards.
- Implementing additional scaling capabilities.

#### Q&A Discussion

When asked how they would recover from pipeline failures, the team highlighted proactive monitoring through CloudWatch logs and operational monitoring processes.

A follow-up question explored how CloudWatch would support recovery efforts. __Suzanne__ explained how alerts could notify administrators when failures occur, while __Yousaf__ expanded on the use of CloudWatch agents and performance thresholds to identify infrastructure or application-level issues before they become critical.

#### General Observations

This presentation stood out for its clear narrative structure and strong emphasis on business value alongside technical implementation. The team demonstrated mature project planning practices and maintained a clear focus on delivering a functional MVP.
