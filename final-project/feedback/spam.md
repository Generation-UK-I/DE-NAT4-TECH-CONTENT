# ETL Project Feedback

## Team: SPAM

### Team Members: Sarah, Pawandeep, Ammad, Maryam

SPAM delivered one of the strongest business-oriented presentations, consistently linking technical decisions back to client needs and organisational outcomes.

#### Project Overview and Delivery

__Pawandeep__ opened the presentation by reviewing the client's requirements and drawing useful connections to lessons learned during the team's previous project work.

__Maryam__ provided a compelling overview of the client's challenges, explaining how organisational growth had created fragmented data sources, limited visibility across operations, and inefficient manual reporting processes. She effectively communicated the business value of creating a unified analytics platform capable of identifying trends and supporting decision-making.

The team's project management approach was comprehensive and well articulated. __Pawandeep__ reviewed their MoSCoW prioritisation strategy, MVP definition, acceptance criteria, and governance processes. Notable practices included:

- Main branch protection within GitHub.
- Structured pull request reviews.
- Regular Product Owner engagement.
- Jira and Confluence for project management.
- Slack for team communication.
- Retrospectives using the "4 Ls" framework (Loved, Longed For, Loathed, Learned).

The team also presented a database relationship diagram, demonstrating consideration of data structure and design.

__Sarah__ explained the end-to-end architecture:

- CSV → S3 → Transform/Clean → Database → SQL Queries → Grafana Dashboards
- She also discussed the AWS services selected, including S3, Lambda, Redshift, and EC2.

__Ammad__ provided a live demonstration of the solution, beginning with source code in Visual Studio Code and progressing through the transformation and loading stages into PostgreSQL using Adminer. He also presented CloudWatch logs confirming successful execution in AWS.

A notable challenge involved Lambda timeout limitations. The team successfully resolved this by adjusting execution timeout configurations. __Ammad__ also highlighted the team's implementation of automated unit tests for deployment scripts, demonstrating good engineering practices.

Further demonstrations included:

- Amazon Redshift cluster deployment.
- Grafana dashboards.
- Multiple visualisations and business-relevant metrics.

#### Reflections and Learning

__Maryam__ discussed current limitations, noting that scalability had not yet been formally tested and that file uploads remained a manual process requiring user interaction.

Future enhancements identified by the team included:

- Automated ingestion mechanisms.
- Behavioural analytics.
- Market basket analysis.
- Improved dashboard functionality.
- Greater use of decoupled architecture patterns.

#### Q&A Discussion

When asked how files were uploaded, Sarah explained that uploads were currently performed manually by authenticated AWS users.
During reflections:

- __Ammad__ highlighted the insight gained through creating and running unit tests.
- __Maryam__ was particularly proud of her understanding of Grafana dashboards and data visualisation.
- __Pawandeep__ reflected on the team's success in configuring AWS services and developing dashboards.

#### General Observations

The team demonstrated strong business analysis skills, good software engineering discipline, and one of the most complete technical demonstrations of the cohort. Their focus on testing, governance, and user value strengthened the overall quality of the presentation.
