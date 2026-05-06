# Task 4.4 — DAX vs. ElastiCache for DynamoDB

> **Time Estimate:** 2-3 hours | **Cost:** ~$0.50/hr (tear down fast!)

## 🎯 What You'll Learn
- DAX — transparent DynamoDB caching (zero code changes)
- ElastiCache Redis — generic cache-aside pattern
- When each is appropriate

## 🧠 DAX vs. ElastiCache

| Feature | DAX | ElastiCache (Redis) |
|---------|-----|-------------------|
| Code changes | **Zero** (swap SDK client) | Write cache-aside logic |
| Data source | DynamoDB only | Any source |
| Cache management | Automatic | Manual (TTL, eviction) |
| Overhead | **Least** | **Most** |
| Best for | Hot `GetItem` reads | Multi-source caching |

> ⚠️ **Gotcha:** DAX caches `Scan`/`Query` results too. Large scans can evict hot `GetItem` data from cache.

## ✅ Completion Checklist
- [ ] Created a DAX cluster and tested with DAX client
- [ ] Compared latency before/after DAX
- [ ] Implemented cache-aside with Redis
- [ ] Documented when each is appropriate
- [ ] **Resources torn down immediately** (these cost money!)
