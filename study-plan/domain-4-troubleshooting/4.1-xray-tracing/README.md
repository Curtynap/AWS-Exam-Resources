# Task 4.1 — X-Ray Distributed Tracing

> **Time Estimate:** 1-2 hours | **Cost:** Free Tier (100k traces/mo)

## 🎯 What You'll Learn
- Active tracing on API Gateway and Lambda
- X-Ray SDK instrumentation and subsegments
- Annotations (filterable/indexed) vs. Metadata (not indexed)
- Sampling rules to control costs

## 🚀 Key Steps

```python
# Instrument your Lambda with X-Ray SDK
from aws_xray_sdk.core import xray_recorder, patch_all

patch_all()  # Auto-instrument all AWS SDK calls as subsegments

def lambda_handler(event, context):
    # Add searchable annotations
    xray_recorder.put_annotation('customerId', 'CUST-001')
    
    # Add non-indexed metadata (for debugging)
    xray_recorder.put_metadata('request', event)
    
    # Create a custom subsegment
    with xray_recorder.in_subsegment('process_order') as subseg:
        subseg.put_annotation('orderId', 'ORD-001')
        # ... your logic here
```

## 🧠 Annotations vs. Metadata

| | Annotations | Metadata |
|-|-------------|----------|
| Indexed? | **Yes** — searchable in console | No |
| Filterable? | **Yes** — `annotation.customerId = "CUST-001"` | No |
| Use for | Key identifiers (customerId, orderId) | Full payloads, debug data |
| Limit | 50 per trace | No practical limit |

## 🧠 Sampling Rules
> Default: 1 req/sec + 5% of additional requests. Customize to control costs.

## ✅ Completion Checklist
- [ ] Enabled active tracing on API Gateway and Lambda
- [ ] Instrumented SDK calls as subsegments
- [ ] Added annotations and metadata
- [ ] Viewed service map and trace timeline
- [ ] Resources torn down
