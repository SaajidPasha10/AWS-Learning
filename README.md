# AWS Serverless Data Processing Platform

A hands-on, end-to-end AWS project designed to build practical **AWS serverless, data engineering, security, networking, Infrastructure as Code, and CI/CD skills**

The project is being built incrementally. Each lab introduces a small number of AWS services, explains the underlying architecture, and then integrates them into the larger system.

---

## 🎯 Project Goals

The project has three primary goals:

1. Build strong practical knowledge of AWS services relevant to DEA-C01.
2. Understand how individual AWS services work together in a production-style architecture.
3. Build a portfolio project demonstrating serverless architecture, IaC, security, and CI/CD.

---

# 🏗️ Target Architecture

The final application will be a serverless document-processing platform.

```text
                                  ┌──────────────┐
                                  │    GitHub    │
                                  └──────┬───────┘
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │ CodePipeline │
                                  └──────┬───────┘
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │  CodeBuild   │
                                  └──────┬───────┘
                                         │
                                         ▼
                                ┌─────────────────┐
                                │ CloudFormation  │
                                └────────┬────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
         ┌──────────┐              ┌─────────────┐             ┌─────────┐
         │ Cognito  │              │ API Gateway │             │   VPC   │
         └────┬─────┘              └──────┬──────┘             └─────────┘
              │                           │
              │ JWT                       │
              └──────────────────────────►│
                                          │
                                          ▼
                                   ┌─────────────┐
                                   │   Lambda    │
                                   │ API Handler │
                                   └──────┬──────┘
                                          │
                              ┌───────────┴───────────┐
                              │                       │
                              ▼                       ▼
                       ┌─────────────┐          ┌─────────────┐
                       │  DynamoDB   │          │     SQS     │
                       │  Metadata   │          │    Queue    │
                       └─────────────┘          └──────┬──────┘
                                                       │
                                                       ▼
                                                ┌─────────────┐
                                                │   Lambda    │
                                                │   Worker    │
                                                └──────┬──────┘
                                                       │
                                          ┌────────────┴────────────┐
                                          │                         │
                                          ▼                         ▼
                                     ┌──────────┐              ┌─────────┐
                                     │    S3    │              │   SNS   │
                                     │ Documents│              │  Topic  │
                                     └──────────┘              └────┬────┘
                                                                    │
                                                          ┌─────────┼─────────┐
                                                          ▼         ▼         ▼
                                                         SQS      Lambda   Notification
```

---

# 🔧 AWS Services

## Compute

* AWS Lambda

## API

* Amazon API Gateway

## Authentication

* Amazon Cognito

## Storage

* Amazon S3

## Database

* Amazon DynamoDB

## Messaging

* Amazon SQS
* SQS Dead Letter Queue
* Amazon SNS

## Security

* AWS IAM

## Networking

* Amazon VPC
* Subnets
* Route Tables
* Internet Gateway
* Security Groups
* VPC Endpoints
* NAT Gateway concepts

## Infrastructure as Code

* AWS CloudFormation

## CI/CD

* GitHub
* AWS CodeBuild
* AWS CodePipeline

## Monitoring

* Amazon CloudWatch

---

# 📚 Learning Path

The project is divided into focused labs.

| #  | Lab                             | Main Concepts                       | Status      |
| -- | ------------------------------- | ----------------------------------- | ----------- |
| 01 | Lambda + API Gateway + DynamoDB | Serverless API, Python, DynamoDB    | ✅ Completed |
| 02 | Cognito                         | User pools, authentication, JWT     | ⏳           |
| 03 | Cognito + API Gateway           | JWT authorization                   | ⏳           |
| 04 | S3                              | Object storage, buckets, objects    | ⏳           |
| 05 | S3 + Lambda                     | Event-driven processing             | ⏳           |
| 06 | SQS                             | Queues, consumers, async processing | ⏳           |
| 07 | SNS                             | Pub/Sub, fan-out                    | ⏳           |
| 08 | IAM                             | Roles, policies, least privilege    | ⏳           |
| 09 | VPC                             | Networking, subnets, routing        | ⏳           |
| 10 | CloudFormation                  | Infrastructure as Code              | ⏳           |
| 11 | CodeBuild                       | Build and test automation           | ⏳           |
| 12 | CodePipeline                    | CI/CD                               | ⏳           |
| 13 | Full Integration                | Complete application                | ⏳           |
| 14 | DEA-C01 Review                  | Exam-focused scenarios              | ⏳           |

---

# 🧠 Architecture Patterns

The final project intentionally demonstrates multiple AWS architecture patterns.

## Synchronous API

```text
Client
  ↓
API Gateway
  ↓
Lambda
  ↓
DynamoDB
  ↓
Response
```

## Asynchronous Processing

```text
Lambda
  ↓
SQS
  ↓
Worker Lambda
```

## Pub/Sub

```text
Publisher
    ↓
   SNS
 ┌──┼──┐
 ↓  ↓  ↓
SQS Lambda Notification
```

## Event-Driven Processing

```text
S3
 ↓
Lambda
 ↓
Processing
```

## Infrastructure as Code

```text
CloudFormation
      ↓
AWS Infrastructure
```

## CI/CD

```text
GitHub
   ↓
CodePipeline
   ↓
CodeBuild
   ↓
CloudFormation
   ↓
AWS
```

---

# 💰 Cost Strategy

The project is designed to keep costs as close to zero as practical.

We will:

* Prefer free-tier-eligible services and configurations.
* Avoid unnecessary infrastructure.
* Avoid NAT Gateway during the initial VPC labs.
* Use small workloads.
* Delete resources after labs when they are no longer required.
* Monitor AWS Billing regularly.

> Free-tier eligibility and pricing can change, so always verify the current AWS pricing/free-tier terms before creating resources.

---

# 🔐 Security Principles

Security will be introduced throughout the project rather than added at the end.

The project will use:

* IAM roles
* Least-privilege policies
* Cognito authentication
* API authorization
* S3 permissions
* Lambda execution roles
* Security groups
* Private networking where appropriate
* CloudFormation-managed infrastructure

We will avoid using broad permissions such as:

```text
AdministratorAccess
```

unless there is a specific learning reason.

---

# 🗂️ Repository Structure

```text
aws-serverless-data-platform/
│
├── README.md
│
├── labs/
│   ├── 01-lambda-api-dynamodb/
│   │   ├── README.md
│   │   └── src/
│   │
│   ├── 02-cognito/
│   ├── 03-cognito-api-gateway/
│   ├── 04-s3/
│   ├── 05-s3-lambda/
│   ├── 06-sqs/
│   ├── 07-sns/
│   ├── 08-iam/
│   ├── 09-vpc/
│   ├── 10-cloudformation/
│   ├── 11-codebuild/
│   └── 12-codepipeline/
│
└── infrastructure/
```

---

# 📈 Project Progress

### Completed

* [x] AWS Lambda
* [x] Python Lambda handler
* [x] API Gateway HTTP API
* [x] DynamoDB table
* [x] IAM Lambda execution role
* [x] DynamoDB PutItem
* [x] POST `/documents`
* [x] Input validation
* [x] Basic CloudWatch logging

### In Progress

* [ ] GET `/documents/{document_id}`
* [ ] Cognito authentication
* [ ] API Gateway JWT authorization

### Upcoming

* [ ] S3 document storage
* [ ] S3 event processing
* [ ] SQS
* [ ] Dead Letter Queue
* [ ] SNS
* [ ] VPC
* [ ] CloudFormation
* [ ] CodeBuild
* [ ] CodePipeline
* [ ] End-to-end deployment
* [ ] DEA-C01 architecture review

---

# 🎓 Certification Focus

The project is designed to reinforce practical concepts relevant to **AWS Certified Data Engineer – Associate (DEA-C01)**, including:

* Data ingestion
* Data storage
* Serverless processing
* Event-driven architectures
* Security
* IAM
* Monitoring
* Infrastructure as Code
* Automation
* CI/CD
* AWS networking

The goal is not simply to memorize AWS services, but to understand **why and when each service is used and how services interact**.
