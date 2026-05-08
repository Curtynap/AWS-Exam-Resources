# Task 4.5 — Lambda Performance Tuning

> **Time Estimate:** 2-3 hours | **Cost:** Free Tier

## 🎯 What You'll Learn
- Lambda Power Tuning (memory vs. cost optimization)
- Provisioned Concurrency for cold start elimination
- Deployment package optimization with layers
- The 1769 MB = 1 vCPU breakpoint

## 🧠 Memory ↔ Performance Relationship

| Memory | vCPU | Network | Typical Use Case |
|--------|------|---------|-----------------|
| 128 MB | Fraction | Low | Tiny, fast functions |
| 512 MB | ~0.3 | Medium | Most web APIs |
| 1769 MB | **1 full vCPU** | High | CPU-bound processing |
| 3008 MB | ~1.7 | High | Heavy computation |
| 10240 MB | 6 | Max | ML inference, media |

> **Exam Tip:** Bumping memory often makes Lambda **cheaper** because it runs faster, consuming fewer GB-seconds.

## 🧠 Cold Start Mitigation

| Strategy | Cost | Effectiveness |
|----------|------|---------------|
| Provisioned Concurrency | $$ (charges when idle) | **Eliminates** cold starts |
| Keep functions warm (ping) | $ (invocation cost) | Reduces frequency |
| Smaller packages | Free | Reduces init time |
| SnapStart (Java only) | Free | Caches initialized snapshots |

## ✅ Completion Checklist
- [ ] Ran Lambda Power Tuning state machine
- [ ] Compared graphs at different memory settings
- [ ] Enabled Provisioned Concurrency on an alias
- [ ] Trimmed deployment package size
- [ ] Resources torn down
