# Task 2.2 — Customer-Managed KMS Encryption

> **Time Estimate:** 1-2 hours | **Cost:** ~$1/mo per key (delete after)

---

## 🎯 What You'll Learn

- Customer-managed key (CMK) creation and rotation
- S3 default encryption with `aws:kms`
- DynamoDB encryption at rest with CMK
- Key policies vs IAM policies
- Envelope encryption and Data Key Caching

---

## 🚀 Key Steps

```bash
# 1. Create a CMK
aws kms create-key --description "DVA Study Key" --query "KeyMetadata.KeyId" --output text

# 2. Enable auto-rotation (rotates annually)
aws kms enable-key-rotation --key-id YOUR_KEY_ID

# 3. Apply to S3 bucket
aws s3api put-bucket-encryption --bucket YOUR_BUCKET \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": "YOUR_KEY_ID"}}]
  }'
```

## 🧠 Envelope Encryption (How KMS Actually Works)

```
KMS Master Key (never leaves KMS)
    │
    ├── GenerateDataKey() → Plaintext Data Key + Encrypted Data Key
    │
    ├── Plaintext Key encrypts your data locally
    │
    └── Store: Encrypted Data Key + Encrypted Data (delete plaintext key)
```

> **Exam Tip:** KMS has request quotas. Use **Data Key Caching** (AWS Encryption SDK) for high-throughput apps.

---

## ✅ Completion Checklist

- [ ] Created a customer-managed KMS key
- [ ] Enabled automatic rotation
- [ ] Applied encryption to S3 and DynamoDB
- [ ] Wrote a key policy granting specific Lambda access
- [ ] Understand envelope encryption flow
- [ ] Resources torn down (schedule key deletion)
