# Task 4.6 — API Gateway Throttling, Caching & Usage Plans

> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

## 🎯 What You'll Learn
- Stage-level and method-level throttling (rate + burst)
- Response caching to reduce backend load
- API keys + Usage Plans for tiered access
- 429 Too Many Requests behavior

## 🚀 Key Steps

```bash
# Create an API key
aws apigateway create-api-key --name "FreeTierPartner" --enabled

# Create a usage plan with throttling
aws apigateway create-usage-plan \
  --name "FreeTier" \
  --throttle burstLimit=10,rateLimit=5 \
  --quota limit=1000,period=DAY
```

## 🧠 Throttling Hierarchy

```
Account Limit (10,000 req/s across all APIs)
  └── Stage Limit (e.g., 5,000 req/s for prod)
       └── Method Limit (e.g., 100 req/s for GET /heavy-report)
            └── Usage Plan Limit (e.g., 10 req/s for Free tier key)
```

## 🧠 Caching
- Cache TTL: 0-3600 seconds (default 300)
- Cache by query string, headers, or path
- Cache invalidation: `Cache-Control: max-age=0` header (requires auth)

## ✅ Completion Checklist
- [ ] Configured stage-level throttling
- [ ] Enabled response caching on GET endpoint
- [ ] Created API key + usage plan
- [ ] Triggered 429 responses by exceeding limits
- [ ] Resources torn down
