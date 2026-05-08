# Bonus Task — Elastic Beanstalk & .ebextensions

> **Exam Weight:** Domain 3 (Deployment)
> **Time Estimate:** 1-2 hours | **Cost:** Free Tier (t2.micro / t3.micro)

---

## 🎯 What You'll Learn

- `eb init` and `eb create` CLI commands
- Modifying environments using `.ebextensions` config files
- Deployment strategies (All at once vs. Rolling vs. Immutable)
- Accessing environment variables from code

---

## 🚀 Key Steps

### Step 1: Create a Simple App

```bash
mkdir dva-eb-app && cd dva-eb-app

# Create a basic Node.js app
cat > app.js << 'EOF'
const http = require('http');
const port = process.env.PORT || 3000;
const greeting = process.env.GREETING || "Hello from Elastic Beanstalk!";

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end(`${greeting}\n`);
});

server.listen(port, () => {
  console.log(`Server running at port ${port}/`);
});
EOF

cat > package.json << 'EOF'
{
  "name": "dva-eb-app",
  "version": "1.0.0",
  "scripts": { "start": "node app.js" }
}
EOF
```

### Step 2: Use .ebextensions

```bash
mkdir .ebextensions

# Add an environment variable via config file
cat > .ebextensions/01-environment.config << 'EOF'
option_settings:
  aws:elasticbeanstalk:application:environment:
    GREETING: "Hello from DVA-C02!"
EOF

# Install a package on the underlying EC2 instance
cat > .ebextensions/02-packages.config << 'EOF'
packages:
  yum:
    htop: []
EOF
```

### Step 3: Deploy via EB CLI

```bash
# Initialize the EB application
eb init -p node.js-20 dva-eb-app --region us-east-1

# Create the environment and deploy (takes a few minutes)
eb create dva-eb-env --instance-types t3.micro

# Open the app in your browser
eb open
```

---

## 🧠 Exam-Critical Concepts

### Deployment Policies
| Policy | Downtime | Speed | Rollback | Best For |
|--------|----------|-------|----------|----------|
| **All at once** | Yes | Fastest | Manual | Dev/Test |
| **Rolling** | No | Slow | Manual | Production, full capacity not needed |
| **Rolling with batch** | No | Slower | Manual | Production, full capacity required |
| **Immutable** | No | Slowest | Automatic | Production, high safety, fresh instances |
| **Traffic Splitting** | No | Gradual | Automatic | Canary testing (e.g. 10% traffic first) |

### `.ebextensions` vs. Saved Configurations
- `.ebextensions`: YAML/JSON files stored *in your source code repository*. They configure instances, software, and AWS resources.
- **Saved Configurations**: Stored in S3, used to recreate environments or spin up replicas without changing source code.

---

## 🧹 Teardown

```bash
eb terminate --all --force
```

---

## ✅ Completion Checklist

- [ ] Initialized an EB app and deployed it
- [ ] Created `.ebextensions` to set environment variables
- [ ] Understand the 5 deployment policies
- [ ] Environment terminated
