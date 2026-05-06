# 00 — AWS Account Setup & Safety Net

> Complete this **before** touching any other task. This is your safety net against surprise bills.

---

## Prerequisites

- [ ] **AWS Account** — [Create one here](https://aws.amazon.com/free/) if you don't have one
- [ ] **AWS CLI v2** installed — [Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [ ] **SAM CLI** installed — [Installation guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [ ] **Docker Desktop** installed (needed for `sam local`) — [Download](https://www.docker.com/products/docker-desktop/)
- [ ] **Python 3.12** or **Node.js 20+** installed (pick one as your primary Lambda runtime)
- [ ] **VS Code** with AWS Toolkit extension installed
- [ ] **Postman** or `curl` available for API testing

---

## Step 1: Create an IAM Admin User (Never Use Root)

```bash
# 1. Log into the AWS Console as ROOT
# 2. Go to IAM → Users → Create user
# 3. Name: "dva-study-admin"
# 4. Attach policy: AdministratorAccess
# 5. Enable console access + programmatic access
# 6. Download the credentials CSV
```

> ⚠️ **Never use your root account for daily work.** Root is for billing and account-level settings only.

---

## Step 2: Configure AWS CLI

```bash
aws configure
# AWS Access Key ID: <from Step 1>
# AWS Secret Access Key: <from Step 1>
# Default region name: us-east-1
# Default output format: json
```

Verify it works:
```bash
aws sts get-caller-identity
```

You should see output like:
```json
{
    "UserId": "AIDAEXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/dva-study-admin"
}
```

---

## Step 3: Set a Billing Alarm (CRITICAL)

This is **non-negotiable**. Set this up before doing anything else.

```bash
# Enable billing alerts in your account first:
# Console → Billing → Billing Preferences → Check "Receive Billing Alerts"

# Then create the alarm via CLI:
aws cloudwatch put-metric-alarm \
  --alarm-name "DVA-Study-Billing-Alarm" \
  --alarm-description "Alert when estimated charges exceed $10" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --threshold 10 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --dimensions Name=Currency,Value=USD \
  --alarm-actions arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:billing-alarm-topic \
  --region us-east-1
```

Or do it via the Console:
1. Go to **CloudWatch** → **Alarms** → **Create alarm**
2. Select metric: **Billing** → **Total Estimated Charge**
3. Threshold: **$10** (or whatever your comfort level is)
4. Notification: Create an SNS topic with your email
5. **Confirm the email subscription!**

---

## Step 4: Create a Dedicated S3 Bucket for Artifacts

```bash
# Replace YOUR_UNIQUE_NAME with something unique (S3 bucket names are global)
aws s3 mb s3://dva-study-YOUR_UNIQUE_NAME-artifacts --region us-east-1
```

This bucket will store:
- SAM deployment artifacts
- CodeBuild output
- Lambda deployment packages
- Screenshots and notes from each lab

---

## Step 5: Verify SAM CLI

```bash
sam --version
# Should show SAM CLI version 1.x.x or newer

# Quick smoke test
mkdir -p /tmp/sam-test && cd /tmp/sam-test
sam init --runtime python3.12 --name hello-test --app-template hello-world --no-tracing --no-application-insights --no-structured-logging
cd hello-test
sam build
sam local invoke HelloWorldFunction --event events/event.json
# Clean up
cd .. && rm -rf /tmp/sam-test
```

---

## Step 6: Set Up Your Project Structure

Your study plan directory structure is already created:

```
study-plan/
├── README.md                          ← Progress tracker
├── 00-account-setup/                  ← You are here
├── domain-1-development/
│   ├── 1.1-serverless-rest-api/       ← First task!
│   ├── 1.2-event-source-mappings/
│   ├── ...
├── domain-2-security/
├── domain-3-deployment/
├── domain-4-troubleshooting/
└── capstone/
```

---

## 🧹 Daily Cleanup Checklist

Run this at the **end of every study session**:

```bash
# List all CloudFormation stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query "StackSummaries[].StackName" --output table

# Delete any stacks you're done with
aws cloudformation delete-stack --stack-name STACK_NAME

# Check for orphaned resources
aws lambda list-functions --query "Functions[].FunctionName" --output table
aws dynamodb list-tables --output table
aws sqs list-queues --output table
aws sns list-topics --output table

# Nuclear option: delete EVERYTHING from today's work
# sam delete  (if you used SAM)
```

---

## ✅ Account Setup Complete!

Once all the boxes above are checked, head to [Task 1.1 — Serverless REST API](../domain-1-development/1.1-serverless-rest-api/) to start building.
