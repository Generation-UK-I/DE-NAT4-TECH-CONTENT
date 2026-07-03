# Comparative Analysis of Data Engineering Team Projects

This report synthesizes the key takeaways, methodologies, challenges, and future plans of five different data engineering teams: **Daily Brew, Espresso Yourself, SPAM, Pipin' Hot, and Roaming Rhubarb.** While each team had its own focus, several common themes emerged regarding the ETL (Extract, Transform, Load) pipeline development in a cloud environment (AWS).

## 🚀 **I. Core Project Goals & Scope**

| Team Name | Primary Goal / Problem Addressed | Key Deliverables Mentioned |
| :--- | :--- | :--- |
| **Daily Brew** | Automate data pipelines from various sources; address initial design flaws. | S3 ingestion, Lambda processing, Grafana monitoring. |
| **Espresso Yourself** | Replace manual store-to-analysis processes with an automated pipeline. | S3 $\rightarrow$ Lambda $\rightarrow$ Redshift (or local DB); adherence to MoSCoW/MVP. |
| **SPAM** | Provide a unified view of slow, non-scalable manual business processes. | CSV $\rightarrow$ S3 $\rightarrow$ Transform/Clean $\rightarrow$ DB $\rightarrow$ Grafana Dashboards. |
| **Pipin' Hot** | Aggregate isolated branch data to identify business trends. | CSV $\rightarrow$ S3 $\rightarrow$ Lambda (E/T/L) $\rightarrow$ Redshift; normalization. |
| **Roaming Rhubarb** | Convert raw, unstructured data into structured, analytics-ready data. | Extract $\rightarrow$ Clean $\rightarrow$ Transform $\rightarrow$ Load; normalized schemas. |

### 🛠️ **II. Technical Stack & Architecture**

All teams heavily utilized **AWS** as their primary infrastructure.

* **Ingestion & Storage:** **Amazon S3** was the universal entry point for raw data (CSV).
* **Compute/Processing:** **AWS Lambda** was the primary mechanism for transformation and loading, though some teams explored local/PoC environments initially.
* **Data Warehousing:** **Amazon Redshift** was a common target for structured data storage (Pipin' Hot, Espresso Yourself, SPAM). Some used local databases (PostgreSQL/Adminer).
* **Orchestration & Configuration:** **CloudFormation** was used by several teams (Roaming Rhubarb, Pipin' Hot, Daily Brew) for infrastructure as code.
* **Visualization & Monitoring:** **Grafana** and **CloudWatch Logs** were heavily featured for demonstrating data quality and pipeline health.

### 🧠 **III. Methodologies & Process**

There was a strong consensus across the projects that modern, iterative methodologies were essential for success.

* **Agile Adoption:** Multiple teams explicitly mentioned adopting Agile practices, including **Scrum ceremonies** (standups, retrospectives) and defining roles.
* **Scope Management:** Use of **MoSCoW** (Must have, Should have, Could have, Won't have) was employed by Espresso Yourself and SPAM to define a Minimum Viable Product (MVP).
* **Collaboration:** **Jira, Confluence, and GitHub** were used for tracking tickets, branching, and communication.
* **Role Rotation:** Some teams (Espresso Yourself, Pipin' Hot) intentionally rotated roles to build comprehensive team experience.

### 🚧 **IV. Common Challenges Encountered**

The most significant learning curve across all projects revolved around the complexity of the cloud and external dependencies:

1. **Cloud Service Complexity:** Integrating and understanding the intricacies of AWS services (Lambda, IAM, CloudFormation) was a major hurdle (James in Daily Brew, Ted in Espresso Yourself).
2. **Resource Limitations:** **Lambda timeouts** and issues with **permissions/credentials** (AWS IAM) were recurrent problems (Ammad in SPAM, Kaleb in Roaming Rhubarb).
3. **Data Integrity:** Handling data types, especially dates and unique identifiers (like UUID), and performing necessary **data cleaning and PII removal** were constant tasks.
4. **Dependency Management:** Difficulty in managing external dependencies, such as the Redshift cluster or credentials controlled outside the team's immediate scope.

### 📈 **V. Key Strengths & Achievements**

* **Business Acumen (SPAM):** The SPAM team stood out for strongly linking technical work back to business needs and client requirements.
* **Process Mastery (Espresso Yourself):** This team demonstrated strong adherence to software engineering practices, successfully implementing full Agile frameworks.
* **Technical Depth (Daily Brew/Pipin' Hot):** These teams focused on the technical depth, showing proficiency in scripting, debugging, and moving from local PoC to cloud deployment.
* **Demonstration (SPAM/Daily Brew):** Several teams excelled at demonstrating their final product via live demos of dashboards and logs.

### 🔮 **VI. Next Steps & Future Improvements**

Future work universally aimed to improve robustness, scalability, and feature set:

* **Scalability & Resilience:** Implementing **SQS** (as suggested by Pipin' Hot and as a planned step for others) to handle load spikes and designing for future scaling.
* **Automation:** Moving beyond manual processes (like manual S3 uploads) toward fully automated triggers.
* **Enhanced Visibility:** Adding **Grafana** or more sophisticated monitoring.
* **Optimization:** Refactoring code (e.g., splitting Lambda functions) and improving data schemas.

---

### **Summary Conclusion**

In essence, all five teams successfully moved through the standard modern data engineering lifecycle: **Problem Definition $\rightarrow$ Design $\rightarrow$ Implementation (PoC/MVP) $\rightarrow$ Testing $\rightarrow$ Reflection.** The projects highlight a consistent trend: while the technical skills in building ETL pipelines are growing, the most significant learning often comes from overcoming the complexities of **cloud governance, permissions, and ensuring the solution meets actual business needs.**
