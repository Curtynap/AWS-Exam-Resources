# Task 2.4 — Parameter Store for Configuration

> **Time Estimate:** 1 hour | **Cost:** Free (Standard parameters)

---

## 🎯 What You'll Learn

- Hierarchical parameter paths (`/myapp/dev/featureFlag/...`)
- SecureString vs String parameter types
- `GetParametersByPath` for bulk retrieval
- CloudFormation `{{resolve:ssm:...}}` syntax

---

## 🚀 Key Steps

```bash
# Create a hierarchy
aws ssm put-parameter --name "/myapp/dev/featureFlag/newCheckout" --value "true" --type String
aws ssm put-parameter --name "/myapp/dev/featureFlag/darkMode" --value "false" --type String
aws ssm put-parameter --name "/myapp/dev/dbEndpoint" --value "mydb.cluster.us-east-1.rds.amazonaws.com" --type String
aws ssm put-parameter --name "/myapp/dev/apiKey" --value "sk_live_abc123" --type SecureString

# Fetch all params for dev environment
aws ssm get-parameters-by-path --path "/myapp/dev" --recursive --with-decryption
```

---

## ✅ Completion Checklist

- [ ] Created hierarchical parameters
- [ ] Used SecureString with KMS encryption
- [ ] Retrieved by path from Lambda
- [ ] Referenced parameter in a CloudFormation template
- [ ] Resources torn down
