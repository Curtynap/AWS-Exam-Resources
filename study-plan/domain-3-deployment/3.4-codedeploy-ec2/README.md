# Task 3.4 — CodeDeploy appspec.yml on EC2

> **Time Estimate:** 2-3 hours | **Cost:** t2.micro Free Tier

## 🎯 What You'll Learn
- CodeDeploy agent installation
- `appspec.yml` lifecycle hooks
- Hook order: BeforeInstall → AfterInstall → ApplicationStart → ValidateService
- Deployment to Auto Scaling Groups

## 🚀 Starter appspec.yml

```yaml
version: 0.0
os: linux

files:
  - source: /
    destination: /opt/myapp

hooks:
  BeforeInstall:
    - location: scripts/stop_server.sh
      timeout: 60
  AfterInstall:
    - location: scripts/install_deps.sh
      timeout: 120
  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 60
  ValidateService:
    - location: scripts/health_check.sh
      timeout: 30
```

## 🧠 Hook Order (MEMORIZE)

`ApplicationStop` → `DownloadBundle` → `BeforeInstall` → `Install` → `AfterInstall` → `ApplicationStart` → `ValidateService`

## ✅ Completion Checklist
- [ ] Installed CodeDeploy agent on EC2
- [ ] Created appspec.yml with lifecycle hooks
- [ ] Triggered a deployment from S3 revision
- [ ] Watched lifecycle events in the console
- [ ] Resources torn down
