# Task 1.4 — DynamoDB Indexes & Query Patterns

> **Exam Weight:** Domain 1 (32%) — Indexes and single-table design are guaranteed exam content.
> **Time Estimate:** 2-3 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- Partition key (PK) + sort key (SK) design for range queries
- Global Secondary Indexes (GSI) — when, why, and the async replication gotcha
- Local Secondary Indexes (LSI) — must be created at table creation
- TTL (Time-to-Live) for automatic data expiration
- How to verify queries don't scan the entire table

---

## 🚀 Step-by-Step Instructions

### Step 1: Create the Orders Table

```bash
aws dynamodb create-table \
  --table-name Orders \
  --attribute-definitions \
    AttributeName=customerId,AttributeType=S \
    AttributeName=orderDate,AttributeType=S \
    AttributeName=status,AttributeType=S \
    AttributeName=totalAmount,AttributeType=N \
  --key-schema \
    AttributeName=customerId,KeyType=HASH \
    AttributeName=orderDate,KeyType=RANGE \
  --global-secondary-indexes \
    '[{
      "IndexName": "StatusDateIndex",
      "KeySchema": [
        {"AttributeName": "status", "KeyType": "HASH"},
        {"AttributeName": "orderDate", "KeyType": "RANGE"}
      ],
      "Projection": {"ProjectionType": "ALL"},
      "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    }]' \
  --local-secondary-indexes \
    '[{
      "IndexName": "CustomerAmountIndex",
      "KeySchema": [
        {"AttributeName": "customerId", "KeyType": "HASH"},
        {"AttributeName": "totalAmount", "KeyType": "RANGE"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }]' \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

### Step 2: Load Sample Data

```bash
# Insert multiple orders for testing
aws dynamodb put-item --table-name Orders --item '{
  "customerId": {"S": "CUST-001"},
  "orderDate": {"S": "2026-01-15T10:30:00Z"},
  "status": {"S": "DELIVERED"},
  "totalAmount": {"N": "49.99"},
  "items": {"L": [{"S": "Widget A"}, {"S": "Widget B"}]},
  "ttl": {"N": "1767225600"}
}'

aws dynamodb put-item --table-name Orders --item '{
  "customerId": {"S": "CUST-001"},
  "orderDate": {"S": "2026-03-20T14:00:00Z"},
  "status": {"S": "SHIPPED"},
  "totalAmount": {"N": "149.99"},
  "items": {"L": [{"S": "Gadget X"}]}
}'

aws dynamodb put-item --table-name Orders --item '{
  "customerId": {"S": "CUST-002"},
  "orderDate": {"S": "2026-02-10T09:00:00Z"},
  "status": {"S": "DELIVERED"},
  "totalAmount": {"N": "299.99"},
  "items": {"L": [{"S": "Premium Widget"}]}
}'

aws dynamodb put-item --table-name Orders --item '{
  "customerId": {"S": "CUST-001"},
  "orderDate": {"S": "2026-04-01T16:45:00Z"},
  "status": {"S": "PENDING"},
  "totalAmount": {"N": "24.99"},
  "items": {"L": [{"S": "Mini Widget"}]}
}'
```

### Step 3: Query the Base Table (PK + SK Range)

```bash
# Get all orders for CUST-001 in 2026 (efficient range query on sort key)
aws dynamodb query \
  --table-name Orders \
  --key-condition-expression "customerId = :cid AND orderDate BETWEEN :start AND :end" \
  --expression-attribute-values '{
    ":cid": {"S": "CUST-001"},
    ":start": {"S": "2026-01-01"},
    ":end": {"S": "2026-12-31"}
  }' \
  --return-consumed-capacity TOTAL
```

**Observe:** `ConsumedCapacity` shows how many RCUs were used — it should be very low (no scan).

### Step 4: Query the GSI (Status Dashboard)

```bash
# Get all DELIVERED orders, sorted by date (uses the GSI)
aws dynamodb query \
  --table-name Orders \
  --index-name StatusDateIndex \
  --key-condition-expression "#s = :status" \
  --expression-attribute-names '{"#s": "status"}' \
  --expression-attribute-values '{":status": {"S": "DELIVERED"}}' \
  --return-consumed-capacity TOTAL
```

### Step 5: Query the LSI (Top Spenders)

```bash
# Get CUST-001's orders sorted by amount (uses the LSI)
aws dynamodb query \
  --table-name Orders \
  --index-name CustomerAmountIndex \
  --key-condition-expression "customerId = :cid" \
  --expression-attribute-values '{":cid": {"S": "CUST-001"}}' \
  --scan-index-forward false \
  --return-consumed-capacity TOTAL
```

### Step 6: Enable TTL

```bash
# Enable TTL on the "ttl" attribute
aws dynamodb update-time-to-live \
  --table-name Orders \
  --time-to-live-specification Enabled=true,AttributeName=ttl
```

---

## 🧠 Exam-Critical Concepts

### GSI vs. LSI — Know the Differences

| Feature | GSI | LSI |
|---------|-----|-----|
| Can be added after table creation? | **Yes** | **No** (must be at creation) |
| Partition key | Different from base table | **Same** as base table |
| Sort key | Any attribute | Different from base table |
| Storage limit | Unlimited | **10 GB per partition** (shared with base) |
| Consistency | **Eventually consistent only** | Supports strongly consistent reads |
| Throughput | Separate RCU/WCU | Shares base table's throughput |
| **Exam gotcha** | Under-provisioned GSI throttles base table writes | 10 GB limit can surprise you |

### TTL + Streams = Free Archiving
> **EXAM TIP:** TTL-expired items appear in DynamoDB Streams as REMOVE events.
> You can trigger a Lambda to archive them to S3 — this is the
> **LEAST operational overhead** approach for data lifecycle management.

---

## 🧹 Teardown

```bash
aws dynamodb delete-table --table-name Orders
```

---

## ✅ Completion Checklist

- [ ] Created table with PK + SK, GSI, and LSI
- [ ] Loaded sample data
- [ ] Queried base table with range on sort key
- [ ] Queried GSI for status-based dashboard
- [ ] Queried LSI for amount-sorted results
- [ ] Verified low RCU consumption (no scans)
- [ ] Enabled TTL
- [ ] Can explain GSI vs LSI trade-offs
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
