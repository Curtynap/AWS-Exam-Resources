# Task 4.2 — CloudWatch Logs Insights & Embedded Metric Format

> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

## 🎯 What You'll Learn
- Embedded Metric Format (EMF) — custom metrics from logs with zero API calls
- CloudWatch Logs Insights queries
- Dashboard creation

## 🚀 EMF in Lambda

```python
import json

def lambda_handler(event, context):
    # Emit a custom metric via EMF (no PutMetricData API needed!)
    print(json.dumps({
        "_aws": {
            "Timestamp": 1234567890,
            "CloudWatchMetrics": [{
                "Namespace": "MyApp",
                "Dimensions": [["Environment"]],
                "Metrics": [{"Name": "OrderTotal", "Unit": "None"}]
            }]
        },
        "Environment": "prod",
        "OrderTotal": 149.99
    }))
```

## 🚀 Logs Insights Query

```sql
fields @timestamp, @message
| filter level = "ERROR"
| stats count() by bin(5m)
| sort @timestamp desc
```

## 🧠 EMF vs. PutMetricData

| | EMF | PutMetricData |
|-|-----|---------------|
| Latency impact | **None** (async log parsing) | Blocks execution |
| API calls | **Zero** | 1 per metric batch |
| Cost risk | High-cardinality dimensions | API call volume |

## ✅ Completion Checklist
- [ ] Emitted EMF metrics from Lambda
- [ ] Verified metrics appear in CloudWatch
- [ ] Wrote Logs Insights queries
- [ ] Pinned a query to a dashboard
