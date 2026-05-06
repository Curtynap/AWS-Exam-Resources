# Task 1.7 — Step Functions Orchestration

> **Exam Weight:** Domain 1 (32%) — Workflow orchestration, Standard vs. Express.
> **Time Estimate:** 2-3 hours | **Cost:** Free Tier (4,000 state transitions/mo)

---

## 🎯 What You'll Learn

- Amazon States Language (ASL) definition
- Choice, Parallel, Map, Wait, and Task states
- Catch/Retry for error handling
- Standard vs. Express workflow trade-offs

---

## 🧠 Standard vs. Express

| Feature | Standard | Express |
|---------|----------|---------|
| Max duration | **1 year** | **5 minutes** |
| Execution model | Exactly-once | At-least-once |
| Best for | Long-running, human approval | High-volume, short tasks |

### 256 KB Payload Limit Between States
> Pass **S3 URIs** instead of raw data between states (claim check pattern).

---

## ✅ Completion Checklist

- [ ] Deployed a Step Functions workflow with Choice, Parallel, and Catch
- [ ] Executed and viewed the visual execution graph
- [ ] Compared Standard vs. Express
- [ ] Resources torn down
