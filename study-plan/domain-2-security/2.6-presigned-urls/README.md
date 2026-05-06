# Task 2.6 — Pre-signed URLs for S3

> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- Generating pre-signed GET and PUT URLs
- Time-limited secure access without sharing credentials
- CORS configuration for browser uploads
- Multipart upload pre-signed URLs for large files

---

## 🚀 Lambda: Generate Pre-signed URLs

```python
import boto3
import json

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    action = event.get('action', 'download')
    bucket = 'dva-study-private-bucket'
    key = event.get('key', 'test-file.txt')
    
    if action == 'download':
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=300  # 5 minutes
        )
    elif action == 'upload':
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket,
                'Key': key,
                'ContentType': 'application/octet-stream'
            },
            ExpiresIn=300
        )
    
    return {'statusCode': 200, 'body': json.dumps({'url': url})}
```

## 🧠 Large File Uploads (Multipart)

> For files > 100MB, use **multipart upload** with separate pre-signed URLs per part. A single pre-signed PUT will time out on unreliable networks.

---

## ✅ Completion Checklist

- [ ] Bucket locked with BlockPublicAccess
- [ ] Generated pre-signed GET URL (expires in 5 min)
- [ ] Generated pre-signed PUT URL (browser upload)
- [ ] Verified expiration works
- [ ] Resources torn down
