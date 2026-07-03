# ETL Project Feedback

## Team: Roaming Rhubarb

### Team Members: Karolina, Jacob, Sam, Kaleb

Roaming Rhubarb presented a technically mature solution that showed strong architectural thinking and consideration for extensibility and maintainability.

#### Project Overview and Delivery

__Karolina__ provided an overview of the client's problem, explaining the need to convert raw operational data into structured, analytics-ready information. She reviewed the fundamental ETL process, covering extraction, cleaning, transformation, and loading activities. The team also highlighted their use of Agile ceremonies, MoSCoW prioritisation, and Jira to support collaboration and delivery.

One challenge identified early in the project was managing AWS permissions and access controls.

__Jacob__ presented the architecture and explained how the team initially developed the solution locally before migrating it into AWS. An interesting design decision was the use of AWS Systems Manager Parameter Store for configuration management.

The team adopted a modular approach, keeping architecture components consistent across both local and cloud deployments. This enabled flexibility for clients who may wish to minimise costs by running locally while retaining the option to scale using AWS services when required.

__Jacob__ also reviewed the database schema, demonstrating a normalised structure designed to support future analytical workloads. The team implemented PII removal as part of the transformation process.

__Sam__ delivered an excellent technical architecture presentation using a diagram that closely resembled industry-standard documentation practices. He clearly explained the responsibilities of each AWS service and how data moved through the ETL pipeline. CloudFormation templates were used to automate infrastructure deployment.

__Kaleb__ discussed the principal technical challenges encountered:

- Lambda execution failures.
- SSM credential management.
- Variations in CSV structure.
- Redshift table configuration.
- Lambda timeout limitations.

The team also demonstrated a recording of the ETL process in operation. Similar to several other groups, some Redshift issues were caused by external factors outside the team's control.

#### Future Improvements

The team identified several enhancement opportunities:

- Amazon SQS integration.
- Grafana dashboards.
- Expanded monitoring and observability.
- Improved handling of larger-scale workloads.

#### Q&A Discussion

When asked what they were most proud of:

- __Karolina__ highlighted her understanding of Amazon Redshift.
- __Sam__ pointed to his increased AWS knowledge.
- __Jacob__ emphasised his experience troubleshooting and resolving errors.
- __Kaleb__ referenced the team's success in systematically diagnosing and resolving technical issues.

When asked how they would handle workloads that exceeded Lambda limitations:

- __Karolina__ suggested adjusting Lambda configuration limits where appropriate.
- __Jacob__ proposed migrating processing workloads to AWS Fargate to support more complex or resource-intensive processing requirements.

#### General Observations

Roaming Rhubarb demonstrated strong architectural awareness and one of the more mature approaches to solution design. Their modular strategy, use of Parameter Store, and consideration of both local and cloud deployment models reflected thinking that extends beyond simply meeting minimum project requirements.
