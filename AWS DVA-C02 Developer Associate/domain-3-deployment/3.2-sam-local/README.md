# Task 3.2 — SAM Local Testing

> **Time Estimate:** 1-2 hours | **Cost:** Free (runs locally)

## 🎯 What You'll Learn
- `sam local invoke` for isolated function testing
- `sam local start-api` for full HTTP path testing
- `sam local generate-event` for realistic event payloads
- Attaching a debugger to step through Lambda code

## 🚀 Key Steps

```bash
sam local invoke MyFunction --event events/event.json
sam local start-api  # then curl http://127.0.0.1:3000/hello
sam local generate-event apigateway aws-proxy > events/apigw-event.json
sam local invoke -d 5858 MyFunction  # Attach VS Code debugger on port 5858
```

> ⚠️ **Gotcha:** SAM local doesn't emulate IAM. Your function may work locally with your admin creds but fail in AWS with a scoped execution role.

## ✅ Completion Checklist
- [ ] Invoked function locally with a test event
- [ ] Started local API and tested with curl
- [ ] Generated realistic event payloads
- [ ] Attached a debugger (optional but recommended)
