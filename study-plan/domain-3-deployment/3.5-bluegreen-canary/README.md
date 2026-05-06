# Task 3.5 — Blue/Green & Canary with Lambda Aliases

> **Time Estimate:** 2-3 hours | **Cost:** Free Tier

## 🎯 What You'll Learn
- Lambda versions and aliases
- CodeDeploy traffic shifting: Canary, Linear, AllAtOnce
- CloudWatch alarm-based automatic rollback
- API Gateway canary stage settings

## 🧠 Deployment Strategies

| Strategy | Behavior |
|----------|----------|
| `AllAtOnce` | 100% traffic immediately |
| `Canary10Percent5Minutes` | 10% for 5 min, then 100% |
| `Linear10PercentEvery1Minute` | 10% more each minute |

> ⚠️ **Gotcha:** Database schema changes must be backward-compatible during canary deployments (V1 and V2 run simultaneously).

## ✅ Completion Checklist
- [ ] Published a Lambda version and created an alias
- [ ] Configured Canary deployment with CodeDeploy
- [ ] Added CloudWatch alarm as rollback trigger
- [ ] Compared with API Gateway canary stage settings
- [ ] Resources torn down
