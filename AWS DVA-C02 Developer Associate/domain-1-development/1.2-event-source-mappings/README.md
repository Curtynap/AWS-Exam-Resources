# Task 1.2 — Lambda Event Source Mappings

> **Exam Weight:** Domain 1 (32%) — Push vs. Poll models are guaranteed exam questions.
> **Time Estimate:** 2-3 hours | **Cost:** Free Tier
> **Prerequisite:** Task 1.1 (uses the same DynamoDB table)

---

## 🎯 What You'll Learn

- **Push model** (S3 → Lambda): S3 invokes Lambda directly
- **Poll model** (DynamoDB Streams → Lambda, SQS → Lambda): Lambda service polls the source
- Batch size tuning and batching windows
- Error handling differences between push and poll

---

## 📁 Files in This Task

```
1.2-event-source-mappings/
├── README.md                    ← You are here
├── template.yaml                ← SAM template with all three event sources
├── src/
│   ├── s3_processor.py          ← Handles S3 object creation events (push)
│   ├── stream_processor.py      ← Handles DynamoDB Streams events (poll)
│   └── sqs_processor.py         ← Handles SQS messages (poll)
└── events/
    ├── s3-put-event.json        ← Sample S3 event for local testing
    └── sqs-event.json           ← Sample SQS event for local testing
```

---

## 🏗️ Architecture

```
                         ┌──────────────────────┐
  ┌──── PUSH ────────────│   S3 Bucket          │
  │  (S3 invokes Lambda) │   s3:ObjectCreated   │
  │                      └──────────────────────┘
  ▼
┌──────────────────┐
│  S3 Processor    │     "S3 calls Lambda synchronously"
│  Lambda          │
└──────────────────┘

                         ┌──────────────────────┐
  ┌──── POLL ────────────│   DynamoDB Stream     │
  │  (Lambda polls       │   NEW_AND_OLD_IMAGES  │
  │   the stream)        └──────────────────────┘
  ▼
┌──────────────────┐
│  Stream Processor│     "Lambda service polls the stream in batches"
│  Lambda          │
└──────────────────┘

                         ┌──────────────────────┐
  ┌──── POLL ────────────│   SQS Queue          │
  │  (Lambda polls       │   Standard Queue     │
  │   the queue)         └──────────────────────┘
  ▼
┌──────────────────┐
│  SQS Processor   │     "Lambda service long-polls SQS"
│  Lambda          │
└──────────────────┘
```

---

## 🚀 Step-by-Step Instructions

### Step 1: Deploy the Stack

```bash
cd study-plan/domain-1-development/1.2-event-source-mappings

sam build
sam deploy --guided
# Stack name: dva-task-1-2-event-sources
# Region: us-east-1
```

### Step 2: Test the S3 Push Event

```bash
# Get the bucket name from stack outputs
export BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name dva-task-1-2-event-sources \
  --query "Stacks[0].Outputs[?OutputKey=='UploadBucketName'].OutputValue" \
  --output text)

# Upload a file — this triggers the S3 processor Lambda
echo "Hello DVA-C02" > test-file.txt
aws s3 cp test-file.txt s3://$BUCKET_NAME/uploads/test-file.txt

# Check the Lambda logs (wait a few seconds)
aws logs tail /aws/lambda/dva-task-1-2-S3ProcessorFunction --since 5m --format short
```

**What to observe:** The S3 notification invoked Lambda synchronously (push model). The event contains the bucket name, object key, and size.

### Step 3: Test the DynamoDB Stream Poll Event

```bash
# Insert an item into the Items table from Task 1.1
aws dynamodb put-item \
  --table-name Items \
  --item '{"itemId": {"S": "stream-test-001"}, "name": {"S": "Stream Test"}, "price": {"N": "19.99"}}'

# Update the item to see both OLD and NEW images
aws dynamodb update-item \
  --table-name Items \
  --key '{"itemId": {"S": "stream-test-001"}}' \
  --update-expression "SET price = :p" \
  --expression-attribute-values '{":p": {"N": "24.99"}}'

# Check stream processor logs
aws logs tail /aws/lambda/dva-task-1-2-StreamProcessorFunction --since 5m --format short
```

**What to observe:** The event contains `eventName` (INSERT/MODIFY/REMOVE) and both `OldImage` and `NewImage` because we chose `NEW_AND_OLD_IMAGES` stream view type.

### Step 4: Test the SQS Poll Event

```bash
# Get the queue URL from stack outputs
export QUEUE_URL=$(aws cloudformation describe-stacks \
  --stack-name dva-task-1-2-event-sources \
  --query "Stacks[0].Outputs[?OutputKey=='ProcessingQueueUrl'].OutputValue" \
  --output text)

# Send messages to the queue
aws sqs send-message --queue-url $QUEUE_URL --message-body '{"orderId": "ORD-001", "amount": 49.99}'
aws sqs send-message --queue-url $QUEUE_URL --message-body '{"orderId": "ORD-002", "amount": 99.99}'
aws sqs send-message --queue-url $QUEUE_URL --message-body '{"orderId": "ORD-003", "amount": 149.99}'

# Check SQS processor logs
aws logs tail /aws/lambda/dva-task-1-2-SQSProcessorFunction --since 5m --format short
```

**What to observe:** Lambda polls SQS and may receive multiple messages in a single invocation (batch). The `batchSize` and `MaximumBatchingWindowInSeconds` control this.

### Step 5: Compare Push vs. Poll in CloudWatch

Go to the CloudWatch Console → Log Groups and compare:
- **S3 Processor:** Each upload triggers exactly one invocation
- **Stream Processor:** Batches of stream records arrive together
- **SQS Processor:** Messages are batched based on your settings

---

## 🧠 Exam-Critical Concepts

### Push vs. Poll Model — Know This Cold

| Feature | Push (S3, SNS, API GW) | Poll (SQS, DynamoDB Streams, Kinesis) |
|---------|----------------------|--------------------------------------|
| Who invokes Lambda? | The source service | Lambda service polls the source |
| Retry behavior | Source retries (2x for async) | Lambda retries until success or expiry |
| Batch support | No (one event per invocation) | Yes (configurable batch size) |
| Concurrency | One invocation per event | One invocation per shard/batch |
| Error handling | Goes to DLQ on source side | Entire batch retries on failure |
| **Exam keyword** | "Event notification" | "Event source mapping" |

### SQS Visibility Timeout Rule
> ⚠️ **EXAM TIP:** The SQS queue's **VisibilityTimeout** must be ≥ **6× your Lambda timeout**.
> If Lambda takes 30 seconds, set VisibilityTimeout to ≥ 180 seconds.
> Otherwise, SQS will make the message visible again while Lambda is still processing it.

### DynamoDB Streams View Types
| View Type | What's Included | Use Case |
|-----------|----------------|----------|
| `KEYS_ONLY` | Just the key attributes | Minimal, trigger-only |
| `NEW_IMAGE` | Full item after change | Most common |
| `OLD_IMAGE` | Full item before change | Audit trails |
| `NEW_AND_OLD_IMAGES` | Both before and after | **Change comparison** (recommended for study) |

### Partial Batch Failure Reporting
> **EXAM TIP:** For SQS event source mappings, enable `ReportBatchItemFailures`.
> This lets you return a list of failed message IDs so only those retry,
> instead of the entire batch being retried (which causes duplicates).

---

## 🧹 Teardown

```bash
# Empty the S3 bucket first (required before stack deletion)
aws s3 rm s3://$BUCKET_NAME --recursive

# Delete the stack
sam delete --stack-name dva-task-1-2-event-sources --no-prompts
```

---

## ✅ Completion Checklist

- [X] S3 upload triggered the S3 Processor Lambda (push model)
- [X] DynamoDB insert/update triggered the Stream Processor Lambda (poll model)
- [X] SQS messages were batched and processed by the SQS Processor Lambda (poll model)
- [X] Compared CloudWatch logs across all three patterns
- [X] Understand why VisibilityTimeout must be 6× Lambda timeout
- [X] Can explain push vs. poll models in your own words
- [X] Resources torn down

---

## 📝 My Summary (Fill In After Completing)

**Date completed:** 2026-05-11
**Key takeaway (2 sentences):**
> I deployed and tested Lambda event source mappings using both Push and Poll models. I learned that Push models (like S3) invoke Lambda directly without batching, while Poll models (like DynamoDB Streams and SQS) actively poll for records and process them in batches.

**Tricky thing I learned:**
> Understanding the difference in error handling: SQS (poll) requires enabling partial batch item failures to avoid retrying an entire batch if only one message fails. Also, ensuring the SQS VisibilityTimeout is at least 6x the Lambda timeout is critical.

**Exam-relevant fact I'll remember:**
> Push = "Event Notification" (S3, API Gateway). Poll = "Event Source Mapping" (SQS, DynamoDB Streams). VisibilityTimeout MUST be >= 6x Lambda Timeout!
