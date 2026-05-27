# Introduction to AWS

In this guide we're going to review some of the key services in AWS, some of which you'll become familiar with by using in your main project.

AWS are the biggest cloud provider, so the more of their common services you're aware of the better.

## Service Categories

There are various ways to categories the different service offerings, most of them fit neatly into one of the IaaS, PaaS, or SaaS categories. Another way to consider them is by what they are used for.

## Compute

These services meet our needs for computer processing. This could be for data transformation, media encoding, gaming, running any type of code, basically anything that you need a computer for. Some of the key services in this category include:

### EC2 (Elastic Compute Cloud)

An IaaS offering, this service allows us to deploy instances (virtual machines) of any specification, at any time, anywhere. You can do anything on an instance that you would do on a physical local server, except actually touch it.

We can choose from many common operating systems (Windows, MacOS, various Linux distributions), along with the number of CPU cores, how much RAM you need, the capacity and type of block storage, and many other options.
  
You can deploy as many servers as you require, and they become available for use in minutes - compared to acquiring a new on-premise server, which could take days or weeks. You can also shut them down in seconds, so that you stop paying for them when not needed.

### Container Services

If you want to run some containers you could deploy an EC2 instance selecting an appropriate OS, install Docker, configure it, and finally you can build your images, containers, and deploy them. ECS allows you to jump straight to the last step.

#### Elastic Container Service (ECS)

ECS is a PaaS service, it gives you some options to select, such as the size of instance to be deployed, which you'll select based on the number/type of containers you intend to run, you can also choose where in your network (VPC) it will be deployed so you can manage access to your containers. Otherwise AWS takes care of the OS, Docker installation and maintenance, and configuration in line with industry best practices. You're simply presented with an environment in which you can launch your containers.

Services which operate like this, ie. where your CSP takes care of the underlying resources and configuration, are known as **managed services**.

- Remember, with PaaS services you are giving up some control for convenience. This means you cannot actually log onto the ECS instance, therefore you cannot enter Docker CLI commands directly. So, where do you create and store your images?

#### Elastic Container Registry (ECR)

To complement ECS we have **ECR** which is where we can create and store our container images, then the containers launched from the images are deployed on ECS.

ECR brings many benefits, such as version control, just like with software, allowing easy rollback to stable versions in case of errors.

#### Elastic Kubernetes Service (EKS)

Sometimes called K8S, Kubernetes is a container orchestration tool, which is very popular for managing large fleets of containers, where Docker's built in functionality can become restrictive. EKS allows you to deploy your Kubernetes clusters to a fully managed AWS PaaS offering.

#### Fargate

A **severless** PaaS option, you simply provide a container image (from ECR), and AWS deploys a container for you. You don't worry about instances, it's just deployed for you.

>There are a number of serverless services available, and of course there is still a server involved somewhere in the background. However you have absolutely no consideration of it, you provide the job, and AWS runs it on whatever available resources they have in their DCs.

### Lambda

Launched in 2014, Lambda is no longer a new service, but it is still considered a very modern approach to architecture, because it represents a revolutionary way to think about software and applications.

Lets say you want to write and run an app, but you don't currently have anything, not even a computer. Ok, so you need to:

- Build a computer
- Install the operating system
- Update and configure the OS
- Configure security and access
- Install your IDE (eg. VSCode)
- Install your chosen programming language
- Install any required dependencies or libraries
- Write your code
- Run/host your app*

>*In reality this last step requires lots of additional steps, including: permitting and managing traffic to your app; purchasing a domain and creating DNS records; creating/hosting an API to execute the app; and many more.

Lambda is a PaaS option, considered a **serverless** compute service. If you don't care where your code runs, as long as it runs, you can use Lambda to jump straight to the last two steps of the above list. It also makes all of the additional complexity of running and hosting your app a lot easier.

We will return to Lambda in more depth, as it will be a key part of your pipeline.

## Compute Lab (1 hour)

Using your AWS Skill Builder account, complete the following lab in which you will deploy, monitor, and manage an EC2 web server.

[Introduction to Amazon EC2](https://skillbuilder.aws/learn/9VNGAHHAUU/introduction-to-amazon-ec2/AJZEJRN2BQ)

## Storage Services

Organisations have a wide variety of data storage needs, and AWS have developed services to meet as many of them as possible.

### Simple Storage Service (S3)

The S3 service is AWS' oldest service, it offers **object-based** storage which can be used for pretty much any purpose from simple file storage, application backends, or for temporarily storing data prior to ingestion into an ELT/ELT pipeline.

S3 is secure, durable, highly available, and scales automatically to the content that you want to add.

To use S3 we create buckets, which are just a container for your objects, to keep them separate from other objects. We can create a folder hierarchy within our bucket to keep our objects organised, either for humans to easily navigate, or to deploy a necessary application folder structure when S3 is the back-end storage.

You can make as many buckets as you want, and they can scale to a functionally unlimited size.

You can make buckets in any global region you wish, so that you can locate it near your customer, for lower latency, but you need to give it a name which is **globally unique**.

#### S3 Objects

Objects are data, most commonly files, in any format. Objects can be from 0 bytes to 5TB in size. Although **objects** can technically be data that isn't in any particular **file** format or type, we typically use the terms interchangeably.

Object-based storage is a data storage architecture where data is stored as discrete units called objects, each containing:

- The data itself (the file)
- Associated metadata (*data* about *data*)
- A globally unique identifier (object key), typically this is comprised of:
  - The globally unique bucket name
  - The path to the object within the bucket's folder structure
  - The object's name (key).

    For this reason objects must have unique paths/names, there are some variations for different use cases, but any specific object may be accessed with a URI similar to this:

    `s3://[bucket-name]/[path]/[object-name]`

#### S3 SLAs

S3 is designed to provide:

- Up to 99.99% availability
- Up to 99.999999999% durability (11x 9s)

>For convenience long values like the one above are often referred to as the number of 9s, otherwise the difference between 10 & 11 nines at a glance might not be obvious.

**99.99% availability** equates to 52.60 minutes of downtime per year.

**99.999999999% durability** means that if you store 10 million objects then you expect to lose a single object of your data every 10,000 years. This is achieved by automatically replicating your objects to across data centers in different availability zones within the selected region.

In practice what this means is that there may be occasions when you're unable to access your objects, but they are still there, and safe (durable).

#### S3 Advanced Features

- Object versioning: A feature that allows you to keep multiple versions of an object within the same bucket. When versioning is enabled, S3 creates a new version of an object every time it is modified or overwritten, allowing you to preserve, retrieve, and restore previous versions of an object.
- Storage class: S3 offers several storage classes (or tiers) for your objects, which allow you to balance cost, durability, and retrieval times.
  - If you already have backup copies of your data, you can choose a tier with less durability, but costs less
  - If you have data which you need to keep, but rarely access, you can choose a tier which offers very low storage costs for your objects, but retrieval can be slow and (relatively) expensive.
- Lifecycle policies: Allow you to manage the lifetime of your files automatically, from creation, through various storage tiers, to deletion
- Encryption at-rest (encrypts your data in storage, as opposed to encryption in-transit, which is done differently).
- MFA Delete: Allows you to ensure that a request to delete an object is verified using multi-factor authentication
- Bucket policies to control who can access them

#### S3 as a Source

One of the most useful features of S3 is the ability to use it as a source for data which is used by other systems and apps. Some of the benefits and use cases for this functionality include:

- S3 can send an "**event**" to notify other AWS services when files are added, deleted or updated
  - This can include **Lambda**, **SQS**, **SNS**, **RedShift** and many others
    - **SNS** = Simple Notification Service, messaging service that enables applications to publish messages to subscribers who can then receive those messages via various many protocols like SMS & email
    - **SQS** = Simple Queue Service, message queuing service that enables decoupled communication between distributed applications, allowing messages to be stored temporarily until they are processed by consumers
    - **RedShift** = A Data Warehouse service - explored elsewhere.
- If those systems fail to respond, some of them will receive a retry
  - For example, if Lambdas are *throttled*, S3 will retry the event for up to 6 hours
- AWS **EMR** Clusters can save data directly in S3
  - EMR = Elastic MapReduce, an AWS flavour of a Hadoop Cluster (another data warehouse)
- AWS **Athena** can run queries directly over structured files in S3
  - Athena is an interactive query service that allows users to analyze data directly in Amazon S3 using standard SQL

### Elastic Block Store (EBS)

Computers need hard disks to persist data, whether physical or virtual. When the computer is communicating with it's attached disks it is not doing so at a file level - the hard disk doesn't care what type of files are stored on it. At a low-level the hard disk storage is split up into millions of tiny fixed-size blocks; Any data you save to the disk is divided across these blocks. Therefore, the hard disks (volumes) attached to your computer are considered block-level storage.

Our EC2 instances require block-level storage volumes like any other computer, and the Elastic Block Store (EBS) is the AWS service which lets us make these volumes.

When we make an instance at least one block-level volume is also created, but we can make additional ones independently to our instances.

EBS allows us to:

- Attach multiple volumes to an instance
- Resize volumes dynamically
- Move volumes between instances
- Separate system and operational data

There are lots of options to configure when creating EBS volumes, the size is an obvious one, but we can also choose whether we want mechanical storage (cheap but slow), or solid state (faster, more expensive), as well as options to specify your performance (IOPs) requirements.

## Storage Lab ( 1 hour)

You may use S3 buckets for various purposes in your pipeline, therefore to get your head around it in the management console first, complete the following storage lab using your Skill Builder account.

[Introduction to Amazon Simple Storage Service (S3)](https://skillbuilder.aws/learn/R54NZHEX5K/introduction-to-amazon-simple-storage-service-s3/SKTY8SPYDX)

## Networking in the Cloud

We will take a look at how networks actually work in an upcoming session, but for now it is worth understanding how we translate the physical cables, switches, and routers from our on-premise infrastructure, to the cloud.

The simple answer is we don't really need to do anything differently. Some of the key components we consider when building networks are:

- **Cables**: Used to physically connect our devices together so they may access the network.
  - Typically copper Ethernet, but on-prem fibre-optic is becoming more common.
  - For our purposes disregard wifi, we never connect a server to the network with wifi.
- **Switches**: These devices include lots of ports into which our devices are connected via cables. So switches effectively 'form' the network.
  - The switch has lots of network ports, it receives traffic in one port, and forwards it out another
  - Almost all network traffic passes through switches.
- **Routers**: As networks become complex, we need to manage where traffic can go, and how it gets there For example the router provides a **route** to the internet.
  - The router allows you to define routes traffic can take, which allows you to permit and deny it. For example, you may want to prevent traffic from reaching an segment of your network (a **subnet**) containing resources with sensitive data.
- **Firewalls**: These devices are used to manage the traffic that is allowed access your network and resources. There are some advanced mechanisms, but at the basic level you can define ports, protocols, and IP addresses which are permitted or denyed access.
  - For example, a web server only operates on `HTTP` and/or `HTTPS`, the firewall allows you to block all traffic except this type.

All of these key components in our networks exist in the cloud, and more. It's just that they're logical, not physical.

- Cables aren't required of course, but every resource we deploy is automatically connected to our network in the cloud (VPC), otherwise we couldn't access it!
- In AWS we can use `Route Tables` to define the routes we add to our physical router
- Since cables aren't needed, we don't need to worry about connecting devices with switches.
  - There is some advanced switch functionality which can be replicated with specialist AWS services.
- Managing traffic in our networks is a crucial requirement, therefore we can implement basic functionality with Security Groups which can be created and configured easily.
  - Advanced firewall functionality is offered by additional AWS services.

### Virtual Private Cloud (VPC)

In our own cloud account we can create a network using the VPC service, which creates a 'virtual network', which we call a VPC, in the cloud. It is a logically isolated environment into which you can deploy your infrastructure resources.

The VPC supports the same addressing schemes* which we've used for decades (IPv4 with support for IPv6), so there will be no issues with traffic between existing & legacy on-prem systems, and your cloud resources.

>*Although with a smaller range of available addresses.

We can also segment our VPC into further logically isolated **subnets**, which allows for greater control over resource placement, and traffic management as mentioned above.

### Route53 (DNS)

The Domain Name Service (DNS) is basically the global '*address book*' for the internet, it allows us to look up a human-friendly domain name, and receive the corresponding IP address for that target.

Just like your home needs a unique address in order to receive post, computers on the internet need a unique address in order to send and receive traffic, this address is called an IP (internet protocol) address.

We'll look into IP addressing in more depth in our networking sessions, for now just know that an IPv4 address looks like this: `213.47.103.73`. Humans are not good at memorising numbers, so if every web server on the internet required you to enter an address like that, we would probably only know about 4 or 5 websites each.

DNS provides us with a system that maps human friendly domain names, to IP addresses, so we can type in an address like www.bbc.co.uk or...


Route 53 is AWS' Domain Name Service (DNS) offering, 


**... to be completed**

## Networking Lab (45 mins)

We'll explore how networks work behind the scenes in a future session, but for now using your Skill Builder account complete the following lab to deploy and configure a VPC.

>Don't worry about memorising everything, we're not here to become cloud architects, just focus on understanding concepts.

[Introduction to Amazon Virtual Private Cloud (VPC)](https://skillbuilder.aws/learn/PH6Z6EVH8Z/introduction-to-amazon-virtual-private-cloud-vpc/PA8H7FUE15)
