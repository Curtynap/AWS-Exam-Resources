# Task 3.3 — CodeBuild buildspec.yml

> **Time Estimate:** 1-2 hours | **Cost:** Free Tier (100 min/mo)

## 🎯 What You'll Learn
- `buildspec.yml` phase order: install → pre_build → build → post_build
- Injecting secrets via `env.parameter-store` and `env.secrets-manager`
- Artifacts and cache configuration

## 🚀 Starter buildspec.yml

```yaml
version: 0.2

env:
  parameter-store:
    DB_ENDPOINT: /myapp/dev/dbEndpoint
  secrets-manager:
    DB_PASSWORD: myapp/db-credentials:password

phases:
  install:
    runtime-versions:
      python: 3.12
    commands:
      - pip install -r requirements.txt
  pre_build:
    commands:
      - echo "Running tests..."
      - python -m pytest tests/ -v
  build:
    commands:
      - echo "Packaging application..."
      - sam build
  post_build:
    commands:
      - echo "Build completed on $(date)"

artifacts:
  files:
    - '**/*'
  base-directory: .aws-sam/build

cache:
  paths:
    - '/root/.cache/pip/**/*'
```

## ✅ Completion Checklist
- [ ] Created buildspec.yml with all four phases
- [ ] Injected parameters and secrets via env block
- [ ] Defined artifacts and cache paths
- [ ] Ran a build successfully in CodeBuild
