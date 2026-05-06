# Bonus Task — Kinesis Data Streams vs. SQS

> **Exam Weight:** Domain 1 (Development)
> **Time Estimate:** 1-2 hours | **Cost:** ~$0.50 (tear down fast!)

---

## 🎯 What You'll Learn

- Streaming data (Kinesis) vs. Queuing (SQS)
- Shards, Partition Keys, and record ordering
- Kinesis Event Source Mapping for Lambda
- `TRIM_HORIZON` vs. `LATEST` starting positions

---

## 🚀 Key Steps

### Step 1: Create a Kinesis Stream

```bash
aws kinesis create-stream \
  --stream-name dva-click-stream \
  --shard-count 2

# Wait for stream to become ACTIVE
aws kinesis describe-stream --stream-name dva-click-stream
```

### Step 2: Put Records

```bash
# Put a single record
aws kinesis put-record \
  --stream-name dva-click-stream \
  --partition-key "user-123" \
  --data "eyJldmVudFR5cGUiOiAiQ0xJQ0sifQ==" # Base64 encoded '{"eventType": "CLICK"}'

# Put another record with the SAME partition key
# (It will go to the same shard, guaranteeing order!)
aws kinesis put-record \
  --stream-name dva-click-stream \
  --partition-key "user-123" \
  --data "eyJldmVudFR5cGUiOiAiU0NST0xMIn0=" # Base64 encoded '{"eventType": "SCROLL"}'
```

### Step 3: Read Records using Shard Iterator

```bash
# 1. Get the Shard ID
aws kinesis list-shards --stream-name dva-click-stream

# 2. Get a Shard Iterator (Starting from oldest records)
aws kinesis get-shard-iterator \
  --stream-name dva-click-stream \
  --shard-id shardId-000000000000 \
  --shard-iterator-type TRIM_HORIZON

# 3. Read the records using the iterator string from the previous step
aws kinesis get-records --shard-iterator <YOUR_SHARD_ITERATOR_STRING>
```

---

## 🧠 Exam-Critical Concepts

### Kinesis vs. SQS (Guaranteed Exam Question)

| Feature | Kinesis Data Streams | Amazon SQS |
|---------|----------------------|------------|
| Data type | Real-time streaming (logs, clicks) | Decoupled messages/tasks |
| Routing | **Partition Key** determines shard | No concept of shards |
| Ordering | Ordered **within a shard** | Best effort (Standard) / Strict (FIFO) |
| Multiple Consumers | Yes (records remain in stream) | No (message deleted after read) |
| Scaling | Manual (add/merge shards) or On-Demand | Automatic |

### Kinesis Consumer Options
1. **Lambda Event Source Mapping**: Lambda polls the stream automatically. Max 10 concurrent Lambdas per shard.
2. **KCL (Kinesis Client Library)**: Java/Python library running on EC2/ECS. It manages shard iterators and uses DynamoDB for checkpointing. 
3. **Enhanced Fan-Out (EFO)**: Pushes records to consumers via HTTP/2, bypassing the 2MB/sec per shard read limit (gives each consumer its own 2MB/sec pipe).

### Starting Positions
- `TRIM_HORIZON`: Start from the oldest available record.
- `LATEST`: Start from records arriving *after* the consumer starts.
- `AT_TIMESTAMP`: Start at a specific time.

---

## 🧹 Teardown

```bash
aws kinesis delete-stream --stream-name dva-click-stream
```

---

## ✅ Completion Checklist

- [ ] Created a Kinesis stream with 2 shards
- [ ] Put records using a Partition Key
- [ ] Retrieved records manually using a Shard Iterator
- [ ] Understand the difference between Kinesis and SQS
- [ ] Resources torn down
