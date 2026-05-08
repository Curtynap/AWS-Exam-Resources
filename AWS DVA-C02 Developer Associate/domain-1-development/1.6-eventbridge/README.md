# Task 1.6 — EventBridge Custom Bus & Schedules

> **Exam Weight:** Domain 1 (32%) — EventBridge has displaced CloudWatch Events on the exam.
> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- Custom event buses vs. the default bus
- Event patterns for routing (source, detail-type, detail matching)
- Schedule expressions (rate and cron)
- Dead-letter queues and retry policies on targets
- The 256 KB payload limit and the "claim check" pattern

---

## 🚀 Step-by-Step Instructions

### Step 1: Create a Custom Event Bus

```bash
aws events create-event-bus --name dva-orders-bus
```

### Step 2: Create a Rule with an Event Pattern

```bash
# Create a rule that matches order events
aws events put-rule \
  --name OrderPlacedRule \
  --event-bus-name dva-orders-bus \
  --event-pattern '{
    "source": ["myapp.orders"],
    "detail-type": ["OrderPlaced"],
    "detail": {
      "amount": [{"numeric": [">", 50]}]
    }
  }' \
  --state ENABLED
```

### Step 3: Publish a Custom Event

```python
# publish_event.py — Run this script to send a test event
import boto3
import json
from datetime import datetime

client = boto3.client('events')

response = client.put_events(
    Entries=[
        {
            'Source': 'myapp.orders',
            'DetailType': 'OrderPlaced',
            'Detail': json.dumps({
                'orderId': 'ORD-100',
                'customerId': 'CUST-001',
                'amount': 149.99,
                'items': ['Widget A', 'Gadget X'],
                'timestamp': datetime.utcnow().isoformat()
            }),
            'EventBusName': 'dva-orders-bus'
        }
    ]
)
print(f"Events sent: {response['Entries']}")
print(f"Failed count: {response['FailedEntryCount']}")
```

### Step 4: Create a Scheduled Rule

```bash
# Run every 5 minutes (rate expression)
aws events put-rule \
  --name ReconciliationSchedule \
  --schedule-expression "rate(5 minutes)" \
  --state ENABLED

# Or use a cron expression (daily at midnight UTC)
# --schedule-expression "cron(0 0 * * ? *)"
```

---

## 🧠 Exam-Critical Concepts

### Event Pattern Matching
```json
{
  "source": ["myapp.orders"],
  "detail-type": ["OrderPlaced"],
  "detail": {
    "amount": [{"numeric": [">=", 100]}],
    "status": ["CONFIRMED", "SHIPPED"]
  }
}
```
> Matches events where `source` is "myapp.orders" AND `amount` ≥ 100 AND `status` is either CONFIRMED or SHIPPED.

### Claim Check Pattern (256 KB Limit)
> EventBridge events cannot exceed **256 KB**. For larger payloads:
> 1. Store the full data in S3
> 2. Put only the S3 URI in the EventBridge event
> 3. Consumers retrieve the data from S3

### Archives & Replays
> EventBridge can **archive** events and **replay** them later for debugging or reprocessing. This is a common exam scenario.

---

## 🧹 Teardown

```bash
aws events remove-targets --rule OrderPlacedRule --event-bus-name dva-orders-bus --ids "1"
aws events delete-rule --name OrderPlacedRule --event-bus-name dva-orders-bus
aws events delete-event-bus --name dva-orders-bus
aws events remove-targets --rule ReconciliationSchedule --ids "1"
aws events delete-rule --name ReconciliationSchedule
```

---

## ✅ Completion Checklist

- [ ] Created a custom event bus
- [ ] Created a rule with a JSON event pattern
- [ ] Published events with PutEvents and verified routing
- [ ] Created a scheduled rule (rate or cron)
- [ ] Added a DLQ and retry policy to a target
- [ ] Understand the 256 KB limit and claim check pattern
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
