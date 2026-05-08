# Task 3.6 — CodePipeline End-to-End

> **Time Estimate:** 2-3 hours | **Cost:** 1 free pipeline

## 🎯 What You'll Learn
- Source → Build → Deploy pipeline stages
- Manual approval actions
- Artifact encryption with customer-managed KMS
- Cross-account deployment considerations

## 🚀 Key Steps

1. Create a GitHub connection (or CodeCommit repo)
2. Create CodePipeline with three stages: Source, Build, Deploy
3. Add a manual approval between Build and Deploy
4. Push a commit and watch the pipeline execute

## 🧠 Cross-Account Pipelines
> ⚠️ Cross-account deployments require:
> - Shared S3 artifact bucket with **customer-managed KMS** (not `aws/s3`)
> - IAM trust relationships between accounts
> - The deployment role in the target account

## ✅ Completion Checklist
- [ ] Built a three-stage pipeline
- [ ] Added manual approval action
- [ ] Encrypted artifacts with KMS
- [ ] Triggered pipeline with a code push
- [ ] Resources torn down
