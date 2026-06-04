# Introduction to Security

Security is about ensuring our systems, resources, and assets remain secure, obviously, but what does that mean?

## CIA & AAA

These two acronyms are useful to summarise our aims and objectives.

### Confidentiality, Integrity, Availability (CIA)

CIA refers to our goal of ensuring our data has:

- Confidentiality: The data is only accessible by those who require it. We typically implement this with access control systems.
- Integrity: This property is about whether you can trust your data. Specifically, can you verify that the data had any unauthorised modification.

  Typically this will be facilitated by integrity checking tools such as hashing
- Availability: This is about ensuring that your data and resources remain accessible. If your systems are inaccessible, then operations may grind to a halt.

### Authentication, Authorisation, Accounting (AAA)

AAA describes the types of security controls we should implement in order to acheive CIA. Every security control we implement should contribute towards one or more of these goals.

- Authentication (Who Are You?): Refers to the method by which you confirm your identity when accessing a system or resource. Typical authentication methods include usernames and passwords along with multi-factor authentication (MFA).

  MFA is about using more than one 'factor' to confirm your identity. There are three factors, with multiple individual methods within each one:

    - Something you know: Includes usernames and passwords, security answers (e.g. mother's maiden name, first pet's name), personal details (e.g. DOB, passport number).
    - Something you are: This covers bio-metrics, most commonly fingerprint and facial recognition, but there are others such as voice print analysis, iris scanning, etc.
    - Something you have: Includes options where you receive a code via text message or email, as well as authenticator apps, all of which require you to have access to your phone.

>Remember, multi-factor authentication requires authentication methods from more than one factor, so username & password, along with a secret answer is not MFA, because it's two things you know, so just one factor.

## Layered security models

Another approach to planning your security posture is to use a layered model, also known as _defense in depth_. There isn't one _official_ model to use, but they all follow the same concept.

The center of the model is your critical data assets, and it is surrounded by different layers of protection, each of which an attacker would have to overcome, in order to access the sensitive data.

#TODO: DIAGRAM

- **Data security** - Controls which focus upon ensuring your data has CIA, including access control, encryption, backup strategies, etc.
- **Application security** - Includes actions like ensuring your code follows security best practices to avoid vulnerabilities such as SQL injection and other common risks (Google "_OWASP Top 10_" and "_CVE List_"), avoid using outdated dependencies and libraries, and so on.
- **Host-based**/**Endpoint Security** - Refers to the security controls implemented upon the systems hosting your data/apps, and the systems used to access them. Common actions include:
  - Instal and configure host-based security tools such as anti-virus, firewall, logging, monitoring, and access control following the **principle of least privilege**.
  - _Harden_ the server by removing unnecessary apps and services
  - Ensure appropriate update and patching strategies are in place.
  - Deploying Mobile Device Management software onto mobiles/laptops
  - Device based encryption e.g. BitLocker.
- **Network Security** - Includes network firewalls, intrusion prevention systems (IPS) which can monitor and block traffic dynamically, network segmentation (subnetting) to isolate sensitive resources.
- **Perimeter Security** - This typically involves strategies deployed at the point at which external traffic enters your network.
  - Perimeter network: an isolated network segment in which you can deploy only the resources which need to be public facing. Then all public traffic is directed into this network, with no route out to any sensitive resources.
  - **Honeypot** - This is a _dummy_ target, which looks like the real thing and is meant to entice attackers. If they take the bait you can carry out your own reconnaissance, identify the attacker and the types of breach(es) they're attempting, allowing you to mitigate and improve your posture.

## Security Lifecycle

Although all of our employees should be considering security at all times, for the cyber security professionals their day to day operations can be summarised and guided by a lifecycle.

![security lifecycle](./img/security%20lifecycle.jpg)

### Prevention

The majority of your time will hopefully be spent in the prevention part of the lifecycle, maintaining and evolving your security posture to mitigate the likelihood of a successful attack.

Some of the actions that occur in the Prevention phase include:

- Discovery: In order to prevent an attack, you need to know what you're protecting. In modern cloud environments your infrastructure can be constantly changing, so you require an inventory of all of your assets and resources, along with the software and versions installed. AWS Systems Manager provides an Inventory utility, and many third party options exist.
- Identify vulnerabilities: Once you know what you need to protect, you can identify what those assets are likely vulnerable to, a common risk is outdated/unpatched software. For example, say a new vulnerability is discovered in `PDFViewer v2.3.7`, you will need to identify whether any of your systems are running that version, and if so implement a fix.

  Many potential vulnerabilities exist, they can be found in software, hardware, firmware, or systems can be operating correctly and securely, but may be exploited in other ways, such as email being used to distribute phishing attempts.

- How a particular vulnerability is mitigated against will depend on the specific issue, the level of risk it introduces, and whether a suitable fix is available. But our common strategies include:
  - Anti-virus/anti-malware
  - Access Control
  - Data Security
  - Employee awareness training

### Detection

In the realm of security, short of completely disconnecting a system from all networks (known as air-gapping) you can never guarantee that your environment is completely secure.

In the world of cyber security we have white hats, and black hats. White people are the 'good team', they are often employees of an organisation, or work for 'bug-bounties' where they are paid for discovering and sharing vulnerabilities with the relevant company/developers.

Black Hats are the malicious parties, who are looking to identify vulnerabilities, but when they do they keep them secret, and either use them themselves, or sell the exploit on the black market. These vulnerabilities are known as **Zero-Day exploits**.

Such vulnerabilities are not yet known to the wider industry, so you cannot protect against them!

Two key components for detecting

### Response

- Isolate
- Notify
- Implement play books

### Analysis

- Early indicators
- missed vulnerabilities



## Encryption

- Symmetric
  - Two generals problem
- Asymmetric
  - PKI
    - Digital certs'

### Controls

Preventative, Detective, Corrective

Administrative, Physical, Technical

## Security in AWS

- Shield
- Inspector
- Guard Duty
- WAF

### Security by Design

- Three tier Architecture
  - Presentation / web
  - App
  - Data

## AWS Identity and Access Management (IAM)

![iam](img/iam.svg)<!-- .element: class="centered" height="350px" -->

When an organisation opens an AWS account and starts deploying resources, they need to permit access to those resource for their employees, other users, and often for other services.

IAM is the primary AWS service for providing and managing access. IAM allows you to create three primary entities to facilitate your management.

### IAM Entities

- **Users:** We create user accounts and assign them to our human users, we may also enforce multi-factor authentication (MFA), password rotation rules, and define permissions by attaching **policies**.
  - The first user account, created when setting up your AWS account, is the **root** user. Similar to Linux, this is the most powerful account, which can carry out any action, and cannot be easily restricted. The root user account credentials should be secured, and not used for daily operations.
  - Some actions can only be carried out by the root user, for example closing the AWS account.
- **Groups:** Groups allow you to make collections of users which align with your business operations, commonly job roles, but they can be anything you want. Groups allow you to manage all of the users within as one unit, including assigning permissions, rather than having to manage each user individually.
  - A group can contain many users, and a user can belong to multiple groups
- **Roles:** A type of temporary user account, you assign the required permission policies to the role, and then allow resources or users from other AWS accounts to take on the role as needed. This allows you to provide access to resources, but without creating additional credentials which could be compromised.

>IAM is free to use - you can create as many users, groups, and roles as you wish - but we cannot create nested groups.

### IAM - Policies

You manage access in AWS by creating policies and attaching them to IAM entities (identity-based) or AWS resources. A policy is an object that, when associated with an identity/resource, defines their permissions. These permissions determine if a request is allowed or denied.

The most common types of policies are:

- Identity based - assigned to users/groups/roles (*these are the resources this user can access*)
- Resource based - assigned directly to our cloud resources (*these are the users that can access this resource*)

Most policies are stored as JSON, here is a simple example:

```json
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "ListObjectsInBucket",
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": ["arn:aws:s3:::bucket-name"]
        },
        {
            "Sid": "AllObjectActions",
            "Effect": "Allow",
            "Action": "s3:*Object",
            "Resource": ["arn:aws:s3:::bucket-name/*"]
        }
    ]
}
```

What do you think this policy does?

<details><summary>Reveal:</summary>

Grant read and write access to Amazon S3 bucket objects

</details>

Policy documents can and will be much more complex, allowing you to define granular permissions across your resources, or in this case S3 objects.

>It is recommended that, like groups, you create policies that align with roles. Then one policy assignment will give a user/group all of the permissions they require.

AWS provide a range of policies, which they have created to align with common job roles, and industry best practices. These are known as **AWS Managed Policies**, and you may use them freely. If you create custom policies they are called **Customer Managed Policies**.

### Federation

These days we have dozens of user accounts, and account bloat can be a problem in the workplace. For example, too many accounts encourages people to use repeated or predictable passwords.

IAM supports Identity Federation, which allows your users to use an existing identity provider (IdP) to access their AWS account. Some common identity providers include Facebook, Google, Microsoft Active Directory, etc.

### IAM Integration

Another big benefit of IAM is its' native integration into and alongside other AWS services.

In an on-premise solution you would likely need to acquire and deploy dozens of independent services and tools, each one of them requiring an authentication method to be configured. Then you need to connect them together manually, troubleshoot and debug comm's and compatibility issues, and then maintain the solution as things change and evolve.

All of AWS' services, and particularly IAM, are all tightly integrated together, allowing them to work seamlessly alongside each other. You can also manage access to your instances, S3 buckets/objects, databases, everything you can deploy, all from one centralised location.

### IAM - Best Practices

- Create **individual** users
- Manage permissions with groups (assign users into groups)
    - e.g. "Admin", "Customers"
- Create one IAM role for each different action users need to perform
    - e.g. "run-stock-report-role", "update-basket-items-role"
- Grant **least privilege** with permissions
- Configure a **strong** password policy
- Enable (enforce) MFA for all users

---

### IAM - Best Practices

- Setup audits with AWS CloudTrail
- CloudTrail logs for exactly who did what, when, and from where
- Use IAM roles to allow users and services to share access to other services
- Rotate security credentials **regularly**
- Restrict privileged access further with conditions (for instance, only allowing a range of IPs that a request must come from)
- Reduce use of root (mostly used for billing and locking down account securely)

An example of a 'condition' you could impose would be, for example, allowing a user to use a certain service but only Mon - Fri.

[Skill Builder: Introduction to IAM](https://skillbuilder.aws/learn/XFPX3M7HAQ/introduction-to-aws-identity-and-access-management-iam/DQJ3N5QRRU)

