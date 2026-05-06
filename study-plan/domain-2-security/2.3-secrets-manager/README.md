# Task 2.3 — Secrets Manager from Lambda

> **Time Estimate:** 1-2 hours | **Cost:** ~$0.40/secret/mo

---

## 🎯 What You'll Learn

- Storing and retrieving secrets securely
- Automatic secret rotation
- Caching secrets outside the handler (cold start optimization)
- Cache-busting on rotation failures

---

## 🚀 Lambda Code with Secret Caching

```python
import json
import boto3
from botocore.exceptions import ClientError

# Cache the secret OUTSIDE the handler (persists across warm invocations)
_cached_secret = None

def get_db_credentials():
    global _cached_secret
    if _cached_secret:
        return _cached_secret
    
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='myapp/db-credentials')
    _cached_secret = json.loads(response['SecretString'])
    return _cached_secret

def lambda_handler(event, context):
    try:
        creds = get_db_credentials()
        # Use creds['username'], creds['password'], creds['host']
    except ClientError as e:
        # Secret rotated? Flush cache and retry
        _cached_secret = None
        creds = get_db_credentials()
```

## 🧠 Secrets Manager vs. Parameter Store

| Feature | Secrets Manager | Parameter Store (Standard) |
|---------|----------------|---------------------------|
| Auto rotation | **Built-in** | No |
| Cost | $0.40/secret/mo | **Free** |
| Max size | 64 KB | 4 KB |
| Best for | DB creds, API keys | Feature flags, config |

---

## ✅ Completion Checklist

- [ ] Stored a JSON secret
- [ ] Enabled automatic rotation
- [ ] Lambda retrieves and caches the secret
- [ ] Cache-bust logic handles rotation
- [ ] Resources torn down
