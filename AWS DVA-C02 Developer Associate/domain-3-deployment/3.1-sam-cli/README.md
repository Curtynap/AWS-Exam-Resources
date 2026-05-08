# Task 3.1 — SAM CLI End-to-End

> **Time Estimate:** 2-3 hours | **Cost:** Free Tier

## 🎯 What You'll Learn
- `sam init`, `build`, `deploy`, `delete`, `sync` commands
- `template.yaml` with `AWS::Serverless::*` resource types
- `Globals` section for shared configuration
- `PermissionsBoundary` for enterprise security

## 🚀 Key Steps

```bash
sam init --runtime python3.12 --name hello-sam --app-template hello-world --no-tracing --no-application-insights --no-structured-logging
cd hello-sam
# Modify template.yaml to add a DynamoDB table
sam build
sam deploy --guided
sam delete
```

## 🧠 SAM CLI Commands (MEMORIZE)

| Command | Purpose |
|---------|---------|
| `sam init` | Scaffold a new project |
| `sam build` | Compile and prepare deployment |
| `sam deploy` | Deploy to AWS via CloudFormation |
| `sam local invoke` | Test function locally |
| `sam local start-api` | Local API Gateway emulator |
| `sam sync` | Hot-deploy changes (dev only) |
| `sam delete` | Tear down the stack |

## ✅ Completion Checklist
- [ ] Initialized a SAM project
- [ ] Modified template with DynamoDB table and env var
- [ ] Built and deployed successfully
- [ ] Deleted the entire stack cleanly
