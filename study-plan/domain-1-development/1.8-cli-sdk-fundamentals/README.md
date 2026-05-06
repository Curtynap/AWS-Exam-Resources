# Task 1.8 — AWS CLI & SDK Fundamentals

> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- CLI pagination (`--starting-token`, `--max-items`)
- SDK pagination with `NextToken` loops
- Exponential backoff with jitter for throttling
- Default Credential Provider Chain order

---

## 🧠 Credential Provider Chain (MEMORIZE THIS)

1. **Environment variables** (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. **Shared credentials file** (`~/.aws/credentials`)
3. **AWS config file** (`~/.aws/config`)
4. **ECS container credentials** (task role)
5. **EC2 instance metadata** (instance profile)

> ⚠️ Stale env vars silently override IAM roles attached to your compute.

## 🚀 Hands-On: Pagination Script

```python
# pagination_demo.py
import boto3

s3 = boto3.client('s3')

# Manual pagination using NextToken pattern
paginator = s3.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(Bucket='YOUR-BUCKET')

for page in page_iterator:
    for obj in page.get('Contents', []):
        print(f"  {obj['Key']} ({obj['Size']} bytes)")
```

## 🚀 Hands-On: Custom Retry with Exponential Backoff

```python
# retry_demo.py
import boto3
from botocore.config import Config

# Override SDK default retry behavior
config = Config(
    retries={
        'max_attempts': 5,
        'mode': 'adaptive'  # adaptive = exponential backoff + jitter
    }
)
dynamodb = boto3.client('dynamodb', config=config)
```

---

## ✅ Completion Checklist

- [ ] Used CLI pagination flags on a large result set
- [ ] Wrote SDK pagination loop with NextToken
- [ ] Configured custom retry strategy
- [ ] Tested credential chain by removing env vars
- [ ] Resources torn down
