# Task 1.1 — Build a Serverless REST API

> **Exam Weight:** Domain 1 (32%) — This is the single most important foundational task.
> **Time Estimate:** 2-3 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- How API Gateway integrates with Lambda (proxy integration)
- CRUD operations against DynamoDB using the AWS SDK
- IAM execution roles for Lambda
- Deploying with SAM (infrastructure-as-code)
- Testing REST endpoints with curl

---

## 📁 Files in This Task

```
1.1-serverless-rest-api/
├── README.md              ← You are here
├── template.yaml          ← SAM template (infrastructure as code)
├── src/
│   └── handler.py         ← Lambda function code (CRUD operations)
├── events/
│   ├── create-item.json   ← Test event: create an item
│   ├── get-item.json      ← Test event: get an item
│   ├── update-item.json   ← Test event: update an item
│   └── delete-item.json   ← Test event: delete an item
└── teardown.sh            ← Cleanup script
```

---

## 🚀 Step-by-Step Instructions

### Step 1: Understand the Architecture

```
Client (curl/Postman)
    │
    ▼
┌─────────────────────┐
│  API Gateway (REST)  │  ← /items and /items/{id}
│  Lambda Proxy Integ. │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Lambda Function    │  ← Routes by HTTP method
│   (Python 3.12)      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   DynamoDB Table     │  ← "Items" table, PK: itemId
│   (On-Demand)        │
└─────────────────────┘
```

### Step 2: Review the Code

Open and read through these files before deploying:
1. **`template.yaml`** — Defines all AWS resources declaratively
2. **`src/handler.py`** — The Lambda function that handles all CRUD operations

### Step 3: Build & Deploy

```bash
# Navigate to this task directory
cd study-plan/domain-1-development/1.1-serverless-rest-api

# Build the SAM application
sam build

# Deploy (first time use --guided for interactive setup)
sam deploy --guided
# Stack name: dva-task-1-1-rest-api
# Region: us-east-1
# Confirm changes: Y
# Allow SAM to create IAM roles: Y
# Save config to samconfig.toml: Y
```

### Step 4: Test Your API

After deployment, SAM will output your API URL. Use it below:

```bash
# Set your API URL (replace with actual output from sam deploy)
export API_URL="https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev"

# CREATE — Add an item
curl -X POST "$API_URL/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "AWS Study Guide", "price": 29.99, "category": "books"}'

# READ — Get the item (replace ITEM_ID with the id from the POST response)
curl "$API_URL/items/ITEM_ID"

# UPDATE — Modify the item
curl -X PUT "$API_URL/items/ITEM_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "AWS Study Guide v2", "price": 34.99, "category": "books"}'

# LIST — Get all items
curl "$API_URL/items"

# DELETE — Remove the item
curl -X DELETE "$API_URL/items/ITEM_ID"

# Verify deletion
curl "$API_URL/items/ITEM_ID"
# Should return 404
```

### Step 5: Test Locally (Optional but Recommended)

```bash
# Test the Lambda function directly with a sample event
sam local invoke ItemsFunction --event events/create-item.json

# Start a local API Gateway emulator
sam local start-api
# Then test with: curl http://127.0.0.1:3000/items
```

### Step 6: Explore in the Console

1. **API Gateway Console** → Find your API → Resources → Click on `/items` → See the Lambda proxy integration
2. **Lambda Console** → Find `ItemsFunction` → Check the configuration, environment variables, execution role
3. **DynamoDB Console** → Find the `Items` table → Explore items → Try the PartiQL editor
4. **CloudWatch Logs** → Find the Lambda log group → Review invocation logs

---

## 🧠 Exam-Critical Concepts

### Lambda Proxy Integration vs. Non-Proxy
| Feature | Proxy Integration | Non-Proxy Integration |
|---------|------------------|----------------------|
| Request format | Full HTTP event passed to Lambda | You define mapping templates (VTL) |
| Response format | Lambda must return `statusCode`, `body`, `headers` | API Gateway transforms the response |
| Flexibility | Less control at API Gateway level | Full request/response transformation |
| **When to use** | **Most common, simplest** | Legacy backends, complex transforms |

### DynamoDB On-Demand vs. Provisioned
| Feature | On-Demand | Provisioned |
|---------|-----------|-------------|
| Pricing | Pay per request | Pay per RCU/WCU provisioned |
| Scaling | Instant, automatic | Must configure auto scaling |
| Best for | **Unpredictable traffic** | Stable, predictable traffic |
| **Exam tip** | Default choice for new tables | Cost-optimal for steady workloads |

### API Gateway 29-Second Timeout
> ⚠️ API Gateway has a **hard 29-second timeout** that cannot be changed. If your Lambda takes longer:
> - Return `202 Accepted` immediately
> - Process asynchronously (SQS, Step Functions)
> - Client polls for result

---

## 🧹 Teardown

```bash
# Delete all resources created by this task
sam delete --stack-name dva-task-1-1-rest-api --no-prompts

# Verify everything is gone
aws dynamodb list-tables --query "TableNames" --output table
aws lambda list-functions --query "Functions[].FunctionName" --output table
```

---

## ✅ Completion Checklist

- [X] SAM template deployed successfully
- [X] POST /items creates a new item in DynamoDB
- [X] GET /items/{id} returns the correct item
- [X] PUT /items/{id} updates the item
- [X] DELETE /items/{id} removes the item
- [X] GET /items/{id} returns 404 for a deleted item
- [X] Reviewed the Lambda execution role in IAM
- [X] Explored CloudWatch Logs for invocation records
- [X] Resources torn down after completion

---

## 📝 My Summary (Fill In After Completing)

**Date completed:** 2026-05-10
**Key takeaway (2 sentences):**
> I successfully deployed a Serverless REST API using AWS SAM to manage infrastructure as code. I learned how API Gateway integrates with Lambda via proxy integration and how to execute CRUD operations against a DynamoDB table.

**Tricky thing I learned:**
> Understanding the proxy integration format and ensuring my Lambda function correctly returned the `statusCode`, `body`, and `headers` in the format that API Gateway expects.

**Exam-relevant fact I'll remember:**
> API Gateway has a hard 29-second timeout that cannot be increased, and on-demand DynamoDB tables are best for unpredictable workloads.
