# Bonus Task — ECS, Fargate, and ECR

> **Exam Weight:** Domain 1 & 3 (Development & Deployment)
> **Time Estimate:** 1-2 hours | **Cost:** Free Tier (ECR) / ~$0.05 (Fargate task)

---

## 🎯 What You'll Learn

- Building a Docker image
- Authenticating and pushing to Amazon ECR (Elastic Container Registry)
- Creating an ECS Task Definition
- Running a Serverless Fargate Task

---

## 🚀 Key Steps

### Step 1: Create an ECR Repository

```bash
aws ecr create-repository --repository-name dva-node-app --region us-east-1
```

### Step 2: Build and Push a Docker Image

Create a simple `Dockerfile` in an empty directory:

```dockerfile
FROM node:20-alpine
WORKDIR /app
RUN echo "console.log('Hello from ECS Fargate!'); setInterval(() => {}, 1000);" > index.js
CMD ["node", "index.js"]
```

Build and push the image:

```bash
# 1. Retrieve an authentication token and authenticate Docker to your ECR registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# 2. Build your Docker image
docker build -t dva-node-app .

# 3. Tag the image
docker tag dva-node-app:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/dva-node-app:latest

# 4. Push the image to AWS
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/dva-node-app:latest
```

### Step 3: ECS Terminology (Exam Critical)

| Term | Meaning | Equivalent To |
|------|---------|---------------|
| **ECR (Elastic Container Registry)** | Where your Docker images are stored | Docker Hub |
| **ECS Task Definition** | A JSON file describing how to run your container (Image URI, CPU, Memory, IAM roles, Ports) | `docker-compose.yml` |
| **ECS Task** | A single running instance of a Task Definition | A running `docker container` |
| **ECS Service** | Ensures a specified number of Tasks are always running, integrates with Load Balancers | Kubernetes Deployment |
| **Fargate** | Serverless compute engine for ECS. AWS manages the underlying EC2 instances. | Lambda (but for containers) |
| **EC2 Launch Type** | You manage the EC2 instances that the containers run on. | - |

### Step 4: IAM Roles for ECS

The exam frequently tests the difference between the two IAM roles associated with an ECS Task:

1. **Task Execution Role:** Used by the ECS agent to *pull the container image* from ECR and *push logs* to CloudWatch.
2. **Task Role:** Used by the *application code inside your container* to access AWS services (e.g., reading from an S3 bucket or DynamoDB).

---

## 🧹 Teardown

```bash
aws ecr delete-repository --repository-name dva-node-app --force
```

---

## ✅ Completion Checklist

- [ ] Created an ECR repository
- [ ] Authenticated Docker with ECR via the AWS CLI
- [ ] Built, tagged, and pushed a Docker image
- [ ] Understand the difference between Task Execution Role and Task Role
- [ ] Understand Task Definition vs. Service
