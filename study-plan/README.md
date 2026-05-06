# DVA-C02 Hands-On Study Plan — Progress Tracker

> **Goal:** Complete each mini-project, capture learnings, then tear down to stay under $5/mo.

---

## ⚡ Quick Start

1. Complete the [Account Setup Guide](./00-account-setup/README.md) first
2. Work through tasks **in order** — later tasks build on earlier ones
3. Each task folder has its own `README.md` with full instructions and starter code
4. Check off tasks below as you complete them

---

## 📊 Progress Dashboard

### Phase 1 — Foundation (Domain 1: Development with AWS Services — 32%)
| # | Task | Est. Time | Cost | Status |
|---|------|-----------|------|--------|
| 1.1 | [Serverless REST API](./domain-1-development/1.1-serverless-rest-api/) | 2-3 hrs | Free Tier | ⬜ |
| 1.2 | [Lambda Event Source Mappings](./domain-1-development/1.2-event-source-mappings/) | 2-3 hrs | Free Tier | ⬜ |
| 1.3 | [API Gateway Mapping Templates (VTL)](./domain-1-development/1.3-api-gateway-vtl/) | 1-2 hrs | Free Tier | ⬜ |
| 1.4 | [DynamoDB Indexes & Query Patterns](./domain-1-development/1.4-dynamodb-indexes/) | 2-3 hrs | Free Tier | ⬜ |
| 1.5 | [SNS → SQS Fan-Out](./domain-1-development/1.5-sns-sqs-fanout/) | 1-2 hrs | Free Tier | ⬜ |
| 1.6 | [EventBridge Custom Bus & Schedules](./domain-1-development/1.6-eventbridge/) | 1-2 hrs | Free Tier | ⬜ |
| 1.7 | [Step Functions Orchestration](./domain-1-development/1.7-step-functions/) | 2-3 hrs | Free Tier | ⬜ |
| 1.8 | [AWS CLI & SDK Fundamentals](./domain-1-development/1.8-cli-sdk-fundamentals/) | 1-2 hrs | Free Tier | ⬜ |

### Phase 2 — Security (Domain 2: Security — 26%)
| # | Task | Est. Time | Cost | Status |
|---|------|-----------|------|--------|
| 2.1 | [Cognito User Pool + Identity Pool](./domain-2-security/2.1-cognito/) | 2-3 hrs | Free Tier | ⬜ |
| 2.2 | [Customer-Managed KMS Encryption](./domain-2-security/2.2-kms-encryption/) | 1-2 hrs | ~$1/mo per key | ⬜ |
| 2.3 | [Secrets Manager from Lambda](./domain-2-security/2.3-secrets-manager/) | 1-2 hrs | ~$0.40/secret/mo | ⬜ |
| 2.4 | [Parameter Store for Configuration](./domain-2-security/2.4-parameter-store/) | 1 hr | Free (Standard) | ⬜ |
| 2.5 | [IAM Roles with Least Privilege](./domain-2-security/2.5-iam-least-privilege/) | 1-2 hrs | Free | ⬜ |
| 2.6 | [Pre-signed URLs for S3](./domain-2-security/2.6-presigned-urls/) | 1-2 hrs | Free Tier | ⬜ |

### Phase 3 — Deployment (Domain 3: Deployment — 24%)
| # | Task | Est. Time | Cost | Status |
|---|------|-----------|------|--------|
| 3.1 | [SAM CLI End-to-End](./domain-3-deployment/3.1-sam-cli/) | 2-3 hrs | Free Tier | ⬜ |
| 3.2 | [SAM Local Testing](./domain-3-deployment/3.2-sam-local/) | 1-2 hrs | Free (local) | ⬜ |
| 3.3 | [CodeBuild buildspec.yml](./domain-3-deployment/3.3-codebuild/) | 1-2 hrs | Free Tier (100 min/mo) | ⬜ |
| 3.4 | [CodeDeploy appspec.yml on EC2](./domain-3-deployment/3.4-codedeploy-ec2/) | 2-3 hrs | t2.micro Free Tier | ⬜ |
| 3.5 | [Blue/Green & Canary with Lambda Aliases](./domain-3-deployment/3.5-bluegreen-canary/) | 2-3 hrs | Free Tier | ⬜ |
| 3.6 | [CodePipeline End-to-End](./domain-3-deployment/3.6-codepipeline/) | 2-3 hrs | 1 free pipeline | ⬜ |
| 3.7 | [CloudFormation Drift & Change Sets](./domain-3-deployment/3.7-cloudformation-drift/) | 1-2 hrs | Free | ⬜ |

### Phase 4 — Troubleshooting & Optimization (Domain 4 — 18%)
| # | Task | Est. Time | Cost | Status |
|---|------|-----------|------|--------|
| 4.1 | [X-Ray Distributed Tracing](./domain-4-troubleshooting/4.1-xray-tracing/) | 1-2 hrs | Free Tier (100k traces) | ⬜ |
| 4.2 | [CloudWatch Logs Insights & EMF](./domain-4-troubleshooting/4.2-cloudwatch-emf/) | 1-2 hrs | Free Tier | ⬜ |
| 4.3 | [CloudWatch Alarms & Composite Alarms](./domain-4-troubleshooting/4.3-cloudwatch-alarms/) | 1 hr | Free Tier (10 alarms) | ⬜ |
| 4.4 | [DAX vs. ElastiCache for DynamoDB](./domain-4-troubleshooting/4.4-dax-elasticache/) | 2-3 hrs | ~$0.50/hr (tear down fast!) | ⬜ |
| 4.5 | [Lambda Performance Tuning](./domain-4-troubleshooting/4.5-lambda-tuning/) | 2-3 hrs | Free Tier | ⬜ |
| 4.6 | [API Gateway Throttling & Caching](./domain-4-troubleshooting/4.6-apigw-throttling/) | 1-2 hrs | Free Tier | ⬜ |

### Bonus — Supplementary Services
| # | Task | Est. Time | Cost | Status |
|---|------|-----------|------|--------|
| B.1 | [Amazon Athena: Query S3 with SQL](./bonus-tasks/athena-s3-queries/) | 1-2 hrs | ~$0.01 (tiny data) | ⬜ |
| B.2 | [Elastic Beanstalk & .ebextensions](./bonus-tasks/elastic-beanstalk-ebextensions/) | 1-2 hrs | Free Tier | ⬜ |
| B.3 | [Kinesis Data Streams vs. SQS](./bonus-tasks/kinesis-data-streams/) | 1-2 hrs | ~$0.50 | ⬜ |
| B.4 | [API Gateway Authorizers](./bonus-tasks/api-gateway-authorizers/) | 1-2 hrs | Free Tier | ⬜ |
| B.5 | [ECS, Fargate, and ECR](./bonus-tasks/ecs-fargate-ecr/) | 1-2 hrs | Free Tier | ⬜ |

### Phase 5 — Capstone
| # | Task | Est. Time | Cost | Status |
|---|------|-----------|------|--------|
| 🏆 | [Serverless Order Platform](./capstone/) | 8-12 hrs | < $5/mo idle | ⬜ |

---

## 🎯 Recommended Study Schedule

| Week | Focus | Tasks |
|------|-------|-------|
| **Week 1** | Core Development | 1.1, 1.2, 1.3, 1.4 |
| **Week 2** | Messaging + CLI | 1.5, 1.6, 1.7, 1.8 |
| **Week 3** | Security Deep Dive | 2.1, 2.2, 2.3, 2.4, 2.5, 2.6 |
| **Week 4** | Deployment Pipelines | 3.1, 3.2, 3.3, 3.4 |
| **Week 5** | Advanced Deployment + Monitoring | 3.5, 3.6, 3.7, 4.1, 4.2 |
| **Week 6** | Optimization + Capstone Start | 4.3, 4.4, 4.5, 4.6, Athena (B.1), Capstone |
| **Week 7** | Capstone Finish + Practice Exams | Capstone, Mock exams |

---

## 📝 After Each Task — Write Your Summary

Use this template after completing each task:

```
### Task X.X — [Name]
**Date completed:** YYYY-MM-DD
**Key takeaway (2 sentences):**
> ...

**Tricky thing I learned:**
> ...

**Exam-relevant fact I'll remember:**
> ...
```
