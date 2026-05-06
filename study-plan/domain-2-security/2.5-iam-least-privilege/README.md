# Task 2.5 — IAM Roles with Least Privilege

> **Time Estimate:** 1-2 hours | **Cost:** Free

---

## 🎯 What You'll Learn

- Instance profiles for EC2
- Lambda execution roles
- Resource-based policy conditions (`aws:SourceVpc`, `aws:SourceArn`)
- IAM Access Analyzer for unused access findings
- ABAC (Attribute-Based Access Control) with tags

---

## 🚀 Key Steps

```bash
# Create a tightly-scoped Lambda execution role
aws iam create-role --role-name dva-items-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach a minimal policy
aws iam put-role-policy --role-name dva-items-lambda-role \
  --policy-name DynamoDBItemsOnly \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
      "Resource": "arn:aws:dynamodb:us-east-1:*:table/Items"
    }]
  }'
```

## 🧠 Confused Deputy Prevention

```json
{
  "Condition": {
    "ArnLike": {"aws:SourceArn": "arn:aws:s3:::my-specific-bucket"},
    "StringEquals": {"aws:SourceAccount": "123456789012"}
  }
}
```

---

## ✅ Completion Checklist

- [ ] Created scoped EC2 instance profile
- [ ] Created minimal Lambda execution role
- [ ] Added resource-based conditions
- [ ] Ran IAM Access Analyzer
- [ ] Resources torn down
