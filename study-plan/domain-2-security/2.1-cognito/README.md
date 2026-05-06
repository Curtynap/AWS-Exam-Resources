# Task 2.1 — Cognito User Pool + Identity Pool

> **Time Estimate:** 2-3 hours | **Cost:** Free Tier (50,000 MAUs)

---

## 🎯 What You'll Learn

- User Pool = authentication (JWTs)
- Identity Pool = AWS credentials (temporary STS)
- Hosted UI for sign-up/sign-in
- Per-user S3 access using `${cognito-identity.amazonaws.com:sub}`

---

## 🚀 Key Steps

1. Create a User Pool with email sign-up and MFA optional
2. Create an Identity Pool federating the User Pool
3. Scope the IAM role to per-user S3 prefixes
4. Sign in, exchange JWT for AWS creds, download an S3 object

## 🧠 Exam-Critical: User Pool vs. Identity Pool

| | User Pool | Identity Pool |
|-|-----------|---------------|
| Purpose | **Authentication** | **Authorization** |
| Produces | JWT tokens (ID, Access, Refresh) | Temporary AWS credentials |
| Use case | "Who is this user?" | "What can this user do in AWS?" |

---

## ✅ Completion Checklist

- [ ] User Pool created with hosted UI
- [ ] Identity Pool federates the User Pool
- [ ] IAM role scoped to per-user S3 prefix
- [ ] Signed in and accessed S3 with temporary credentials
- [ ] Resources torn down
