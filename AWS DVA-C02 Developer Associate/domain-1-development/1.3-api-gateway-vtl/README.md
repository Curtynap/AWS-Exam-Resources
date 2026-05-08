# Task 1.3 — API Gateway Mapping Templates (VTL)

> **Exam Weight:** Domain 1 (32%) — VTL and proxy vs. non-proxy integration are classic exam topics.
> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- Non-proxy (custom) integration vs. proxy integration
- Velocity Template Language (VTL) basics
- Request/response transformation at the API Gateway layer
- CORS header handling in non-proxy integrations

---

## 🚀 Step-by-Step Instructions

### Step 1: Deploy the Stack

```bash
cd study-plan/domain-1-development/1.3-api-gateway-vtl
sam build && sam deploy --guided
# Stack name: dva-task-1-3-vtl
```

### Step 2: Test the Request Template

The request VTL template extracts query parameters and reshapes them:

**Input:** `GET /transform?name=Curtis&category=books`

**VTL Template converts this to Lambda input:**
```json
{
  "searchName": "Curtis",
  "searchCategory": "books",
  "requestId": "abc-123"
}
```

```bash
export API_URL="https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev"

# Test with query parameters
curl "$API_URL/transform?name=Curtis&category=books"
```

### Step 3: Test the Response Template

The response VTL template wraps Lambda output with an envelope:

**Lambda returns:** `{"items": [...]}`

**VTL Template reshapes to:**
```json
{
  "statusCode": 200,
  "data": {"items": [...]},
  "requestId": "abc-123",
  "timestamp": "2026-05-06T..."
}
```

### Step 4: Debug with Execution Logs

```bash
# Enable execution logging on the stage (shows VTL processing)
aws apigateway update-stage \
  --rest-api-id YOUR_API_ID \
  --stage-name dev \
  --patch-operations "op=replace,path=/*/logging/loglevel,value=INFO"

# Check the logs
aws logs tail "API-Gateway-Execution-Logs_YOUR_API_ID/dev" --since 5m
```

---

## 🧠 Exam-Critical Concepts

### When to Use Each Integration Type

| Scenario | Integration Type |
|----------|-----------------|
| Simple Lambda backend, full control in code | **Lambda Proxy** (most common) |
| Transform requests before reaching Lambda | **Lambda Non-Proxy** + VTL |
| Return static responses without Lambda | **Mock Integration** + VTL |
| Integrate with any HTTP backend | **HTTP Proxy** or **HTTP Non-Proxy** |
| Call AWS services directly (no Lambda) | **AWS Service Integration** |

### VTL Cheat Sheet

```velocity
## Access query string parameters
$input.params('paramName')

## Access path parameters
$input.params('id')

## Access the full request body
$input.body

## Parse JSON body and access fields
#set($body = $input.path('$'))
$body.fieldName

## Access headers
$input.params().header.get('Authorization')

## Set response header
#set($context.responseOverride.header.X-Custom = "value")

## Context variables (always available)
$context.requestId
$context.stage
$context.identity.sourceIp
```

### CORS with Non-Proxy Integration
> ⚠️ With proxy integration, your Lambda returns CORS headers in its response.
> With non-proxy integration, you must configure CORS headers in the
> **Integration Response** mapping template AND add an OPTIONS method.

---

## 🧹 Teardown

```bash
sam delete --stack-name dva-task-1-3-vtl --no-prompts
```

---

## ✅ Completion Checklist

- [ ] Created a non-proxy Lambda integration
- [ ] Wrote a request VTL template that transforms query params to JSON body
- [ ] Wrote a response VTL template that wraps output in an envelope
- [ ] Tested via the API Gateway Test console
- [ ] Enabled and reviewed execution logs
- [ ] Can explain when to use proxy vs. non-proxy integration
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
