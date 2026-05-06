# Task 1.5 — SNS → SQS Fan-Out

> **Exam Weight:** Domain 1 (32%) — Fan-out is the canonical decoupling pattern.
> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- Publish/subscribe pattern with SNS
- Fan-out to multiple SQS consumers
- SNS subscription filter policies
- Dead-letter queues for guaranteed delivery
- Idempotent message processing

---

## 🚀 Step-by-Step Instructions

### Step 1: Deploy the Stack

```bash
cd study-plan/domain-1-development/1.5-sns-sqs-fanout
sam build && sam deploy --guided
# Stack name: dva-task-1-5-fanout
```

### Step 2: Publish Test Events

```bash
# Get the topic ARN from stack output
export TOPIC_ARN=$(aws cloudformation describe-stacks \
  --stack-name dva-task-1-5-fanout \
  --query "Stacks[0].Outputs[?OutputKey=='OrderEventsTopicArn'].OutputValue" \
  --output text)

# Publish an order event (both queues receive it)
aws sns publish \
  --topic-arn $TOPIC_ARN \
  --message '{"orderId": "ORD-001", "amount": 99.99, "type": "PURCHASE"}' \
  --message-attributes '{"eventType": {"DataType": "String", "StringValue": "order.placed"}}'

# Publish a refund event (only BillingQueue receives it via filter policy)
aws sns publish \
  --topic-arn $TOPIC_ARN \
  --message '{"orderId": "ORD-001", "amount": 99.99, "type": "REFUND"}' \
  --message-attributes '{"eventType": {"DataType": "String", "StringValue": "order.refunded"}}'
```

### Step 3: Verify Fan-Out

```bash
# Check both queue depths
aws sqs get-queue-attributes \
  --queue-url $ANALYTICS_QUEUE_URL \
  --attribute-names ApproximateNumberOfMessages

aws sqs get-queue-attributes \
  --queue-url $BILLING_QUEUE_URL \
  --attribute-names ApproximateNumberOfMessages
```

### Step 4: Check Lambda Consumer Logs

```bash
aws logs tail /aws/lambda/dva-task-1-5-analytics-consumer --since 10m
aws logs tail /aws/lambda/dva-task-1-5-billing-consumer --since 10m
```

---

## 🧠 Exam-Critical Concepts

### SNS Filter Policy Example
```json
{
  "eventType": ["order.placed", "order.shipped"]
}
```
> Only messages with matching `eventType` message attribute reach this subscriber.
> Messages without the attribute are **filtered out** (not delivered).

### At-Least-Once Delivery
> ⚠️ **Standard SQS delivers messages at least once.** Your Lambda consumers
> MUST be idempotent. Use the `messageId` as a deduplication key in DynamoDB.

### Fan-Out Architecture
```
Producer → SNS Topic ──┬──→ SQS (Analytics) → Lambda
                        ├──→ SQS (Billing)   → Lambda  
                        └──→ SQS (Inventory)  → Lambda
```
> Each SQS queue gets its own copy of the message. Each Lambda processes independently.

---

## 🧹 Teardown

```bash
sam delete --stack-name dva-task-1-5-fanout --no-prompts
```

---

## ✅ Completion Checklist

- [ ] SNS topic created with two SQS subscribers
- [ ] Filter policies applied to route events selectively
- [ ] Published messages fan out to correct queues
- [ ] Lambda consumers process messages from each queue
- [ ] DLQs configured for failed messages
- [ ] Understand at-least-once delivery and idempotency
- [ ] Resources torn down

---

## 📝 My Summary (Fill In After Completing)

**Date completed:**
**Key takeaway (2 sentences):**
>

**Tricky thing I learned:**
>

**Exam-relevant fact I'll remember:**
>
