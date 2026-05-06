# Task 4.3 — CloudWatch Alarms & Composite Alarms

> **Time Estimate:** 1 hour | **Cost:** Free Tier (10 alarms)

## 🎯 What You'll Learn
- Metric alarms with thresholds
- Composite alarms for multi-signal alerting
- Anomaly detection for dynamic thresholds
- Treat-missing-data settings

## 🚀 Key Steps

```bash
# Create an error alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "LambdaErrors" \
  --metric-name Errors --namespace AWS/Lambda \
  --statistic Sum --period 300 --threshold 5 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:alerts

# Create a composite alarm
aws cloudwatch put-composite-alarm \
  --alarm-name "CriticalIssue" \
  --alarm-rule "ALARM(LambdaErrors) AND ALARM(LambdaThrottles)"
```

## 🧠 treat-missing-data Options

| Setting | Behavior |
|---------|----------|
| `missing` | Alarm stays in current state |
| `notBreaching` | Treat missing data as OK |
| `breaching` | Treat missing data as alarm |
| `ignore` | Skip evaluation |

## ✅ Completion Checklist
- [ ] Created metric alarm on Lambda errors
- [ ] Created composite alarm combining two alarms
- [ ] Triggered the alarm by erroring a function
- [ ] Resources torn down
