# Task 3.7 — CloudFormation Drift & Change Sets

> **Time Estimate:** 1-2 hours | **Cost:** Free

## 🎯 What You'll Learn
- Drift detection for manual changes
- Change sets to preview modifications
- `DeletionPolicy: Retain` for stateful resources
- Intrinsic functions: `!Ref`, `!Sub`, `!GetAtt`, `!ImportValue`

## 🚀 Key Steps

```bash
# 1. Deploy a stack
aws cloudformation deploy --template-file template.yaml --stack-name dva-drift-test

# 2. Manually modify a resource in the console (e.g., add a tag)

# 3. Detect drift
aws cloudformation detect-stack-drift --stack-name dva-drift-test
aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id ID

# 4. Create a change set before updating
aws cloudformation create-change-set \
  --stack-name dva-drift-test \
  --change-set-name my-changes \
  --template-body file://template-v2.yaml
```

## 🧠 DeletionPolicy Options

| Policy | Behavior |
|--------|----------|
| `Delete` | Resource deleted with stack (DEFAULT) |
| `Retain` | Resource preserved after stack deletion |
| `Snapshot` | Creates snapshot before deletion (RDS, EBS) |

> ⚠️ **Exam Gotcha:** Changing a DynamoDB `TableName` property causes a **Replacement** — the old table is deleted and a new one created. Without `DeletionPolicy: Retain`, all data is lost.

## ✅ Completion Checklist
- [ ] Deployed a stack and manually modified a resource
- [ ] Ran drift detection and reviewed results
- [ ] Created and executed a change set
- [ ] Applied DeletionPolicy: Retain to a stateful resource
- [ ] Resources torn down
