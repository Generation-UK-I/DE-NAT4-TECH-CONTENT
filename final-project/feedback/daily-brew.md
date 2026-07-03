# ETL Project Feedback

## Team: Daily Brew

### Team Members: Ammar, James, Mohammed A, Dilrukshi

Daily Brew presented a well-structured ETL solution, with each team member contributing to different aspects of the project. The team demonstrated a clear understanding of the client's requirements and the challenges involved in delivering a cloud-based data pipeline.

#### Project Overview and Delivery

__Dilrukshi__ opened the presentation by outlining the client's problem and explaining the team's planning and project management approach. The team made effective use of both Jira and collaborative whiteboarding tools to organise work and manage progress throughout the project lifecycle. She highlighted that designing the pipeline proved more challenging than initially anticipated, particularly due to incorrect assumptions regarding Lambda functionality and the complexities involved in integrating multiple AWS services. Grafana integration also presented difficulties that required additional investigation and troubleshooting.

__Ammar__ demonstrated the application code and reviewed the deployed AWS services through the AWS Management Console. He provided a walkthrough of the deployment scripts and demonstrated how raw CSV data was uploaded into Amazon S3 as the first stage of the pipeline.

__James__ explained the team's experience developing the Lambda functionality in Python. A key learning point was discovering that the Lambda trigger configuration was defined within the CloudFormation template rather than the function code itself. The team ultimately decided to rebuild parts of the solution from scratch, finding this approach more efficient than attempting to debug an increasingly complex implementation.

__Mohammed__ presented screenshots of the Grafana dashboards and visualisation layer. James then returned to explain the overall ETL architecture, clearly describing the role of key services including Amazon S3, AWS Lambda, Amazon Redshift, and EC2.

Mohammed also discussed the application's data processing functionality, including the team's approach to identifying and removing personally identifiable information (PII) during the transformation stage.
Reflections and Learning

__Ammar__ reflected candidly on the development journey, noting that until approximately Week 3 the solution only functioned under specific conditions. This demonstrated resilience and persistence in overcoming technical challenges. The team also leveraged AI tools to assist with rewriting and improving Lambda functions, showing a pragmatic approach to problem-solving.
Looking ahead, the team identified several potential enhancements, including:

- Increased automation throughout the pipeline.
- Support for multiple CSV schemas and data structures.
- Greater flexibility in handling varying client datasets.

#### Q&A Discussion

When asked how they would secure the pipeline, the team explained that AWS authentication and access controls would be used to restrict access to authorised users.

In response to questions around scalability, the team proposed processing data in batches to improve throughput and reduce bottlenecks as data volumes increase.

When discussing their proudest achievements:

- __Ammar__ highlighted the knowledge and technical skills gained during the project.
- __James__ echoed this sentiment, focusing on the learning process.
- __Mohammed__ emphasised his increased understanding of ETL workflows and AWS services.

#### General Observations

The team demonstrated strong technical understanding and honesty regarding project challenges. __James__ assumed a leading role during the questioning phase and contributed significantly to many of the responses. Encouraging wider participation during Q&A would help showcase the expertise of all team members.
