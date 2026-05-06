# 🏆 Capstone — Serverless Order Platform

> **Time Estimate:** 8-12 hours | **Cost:** < $5/mo idle
> **Prerequisite:** Complete at least Tasks 1.1–1.5, 2.1–2.3, 3.1, 4.1

---

## 🎯 Objective

Combine **at least nine** services into one SAM-deployed application that exercises every DVA-C02 exam domain.

---

## 🏗️ Architecture

```
                    ┌──────────┐
                    │ Cognito  │  ← Authenticates users (JWTs)
                    │ User Pool│
                    └────┬─────┘
                         │ JWT
                    ┌────▼─────────────────┐
                    │  API Gateway (REST)   │  ← Usage Plans: Free=100/min, Enterprise=5000/min
                    │  POST /orders         │
                    │  GET /orders/{id}     │
                    └────┬─────────────────┘
                         │
                    ┌────▼─────────────────┐
                    │  Lambda (OrderHandler)│  ← Encrypts PII with KMS before writing
                    │                      │  ← Fetches secrets from Secrets Manager (cached)
                    └────┬─────────────────┘
                         │
                    ┌────▼─────────────────┐
                    │  DynamoDB (Orders)    │  ← On-demand, KMS at-rest encryption
                    │  DynamoDB Streams     │
                    └────┬─────────────────┘
                         │ Stream
                    ┌────▼─────────────────┐
                    │  Lambda (PublishEvent)│
                    └────┬─────────────────┘
                         │
                    ┌────▼─────────────────┐
                    │  SNS (OrderEvents)    │  ← Fan-out
                    └────┬────────┬────────┘
                         │        │
              ┌──────────▼─┐  ┌──▼──────────┐
              │ SQS Billing│  │SQS Analytics│
              │ Queue + DLQ│  │Queue + DLQ  │
              └──────┬─────┘  └──────┬──────┘
                     │               │
              ┌──────▼─────┐  ┌──────▼──────┐
              │ Lambda     │  │ Lambda      │
              │ (Billing)  │  │(Analytics)  │
              │ Idempotent │  └─────────────┘
              └────────────┘

  EventBridge Scheduler ──→ Nightly Reconciliation Lambda
  S3 ──→ Media Upload (Pre-signed URLs) ──→ Lambda (Thumbnails)
  X-Ray ──→ Distributed Tracing (5% sampling)
  CloudWatch ──→ Composite Alarm (Errors AND Latency)
  CodePipeline ──→ Source → Build → Canary Deploy
```

---

## 📋 Acceptance Criteria

- [ ] All resources defined in a single SAM template (no console clicks)
- [ ] No hard-coded secrets — everything via Secrets Manager or Parameter Store
- [ ] Failed payment triggers SQS DLQ and CloudWatch alarm fires
- [ ] X-Ray service map shows full path: API GW → Lambda → DynamoDB → SNS → SQS → Lambda
- [ ] Code push to `main` deploys safely via canary with auto-rollback
- [ ] Total monthly cost in idle state below $5

---

## 📁 Suggested Structure

```
capstone/
├── template.yaml              ← Full SAM template
├── samconfig.toml             ← Deployment config
├── src/
│   ├── order_handler.py       ← POST/GET /orders
│   ├── publish_event.py       ← DynamoDB Stream → SNS
│   ├── billing_processor.py   ← SQS billing with idempotency
│   ├── analytics_processor.py ← SQS analytics
│   ├── media_processor.py     ← S3 thumbnail generation
│   └── reconciliation.py      ← Nightly EventBridge job
├── buildspec.yml              ← CodeBuild spec
└── tests/
    └── test_order_handler.py  ← Unit tests
```

---

## 🚀 Build Order

1. Start with `template.yaml` — DynamoDB + Lambda + API Gateway
2. Add Cognito authentication
3. Add KMS encryption and Secrets Manager
4. Add DynamoDB Streams → SNS → SQS fan-out
5. Add EventBridge scheduler
6. Add S3 media upload with pre-signed URLs
7. Add X-Ray tracing and CloudWatch alarms
8. Add CodePipeline CI/CD with canary deployment
9. Test the full flow end-to-end
10. Run `sam delete` to verify clean teardown
