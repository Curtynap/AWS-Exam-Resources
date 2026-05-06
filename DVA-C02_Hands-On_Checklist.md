# AWS Certified Developer – Associate (DVA-C02) Hands-On Checklist

A practical, build-it-yourself study guide. Each task is a mini-project you can execute in your own AWS account. Check the boxes as you go, and read the **Exam Mapping** note for each item to understand *why* it matters on the test.

> **Cost discipline:** spin resources up, complete the task, capture screenshots/code, then tear down. Use the AWS Free Tier where possible and set a billing alarm before you start.

---

## Domain 1 – Development with AWS Services (32%)

### 1.1 Build a Serverless REST API
- [ ] **Objective:** Create a fully functional REST API backed by Lambda and DynamoDB.
- **Services:** API Gateway (REST), AWS Lambda, Amazon DynamoDB, IAM
- **Steps:**
  - Create a DynamoDB table `Items` with partition key `itemId` (String) using on-demand capacity.
  - Author a Python or Node.js Lambda function that performs `GetItem`, `PutItem`, `UpdateItem`, and `DeleteItem` using the AWS SDK.
  - Build a REST API in API Gateway with `/items` and `/items/{id}` resources, wired up with **Lambda proxy integration**.
  - Deploy to a `dev` stage and test each verb (GET, POST, PUT, DELETE) with `curl` or Postman.
- **Implementation Nuance & Trickiness:** 
  - **Varying Data Volume:** On-Demand capacity is ideal for unpredictable traffic. If traffic stabilizes, switch to Provisioned with Auto Scaling for cost savings. 
  - **Trickiness:** API Gateway has a hard 29-second timeout limit. If handling massive payloads or long processing, you must switch to an asynchronous pattern (e.g., returning a 202 Accepted and processing via SQS) rather than a synchronous API call.
- **Exam Mapping:** Tests integration patterns between API Gateway and Lambda, request/response handling, and DynamoDB SDK usage – all heavily weighted in Domain 1.

### 1.2 Lambda Event Source Mappings
- [ ] **Objective:** Trigger a Lambda function from multiple event sources (push and poll models).
- **Services:** AWS Lambda, Amazon S3, Amazon DynamoDB Streams, Amazon SQS
- **Steps:**
  - Create an S3 bucket and configure an `s3:ObjectCreated:*` notification that invokes a Lambda function.
  - Enable a DynamoDB stream (`NEW_AND_OLD_IMAGES`) on the table from 1.1 and create an event source mapping to a second Lambda.
  - Create a standard SQS queue and a third Lambda with an SQS event source mapping; tune the batch size and `MaximumBatchingWindowInSeconds`.
  - Compare invocation logs: notice that S3 is **push** (synchronous) while DynamoDB Streams and SQS use **poll-based** event source mappings.
- **Implementation Nuance & Trickiness:**
  - **Data Surges & Media Processing:** Tuning `BatchSize` and `MaximumBatchingWindowInSeconds` is crucial for handling massive spikes. Additionally, when using S3 event notifications for media (e.g., triggering Lambda for image thumbnails or short audio transcripts), ensure you account for payload limits.
  - **Trickiness:** For large video/audio transcodes that exceed Lambda's 15-minute timeout, S3 events should trigger AWS Step Functions or AWS Elemental MediaConvert instead. For SQS, the queue's visibility timeout *must* be at least 6x the Lambda timeout.
- **Exam Mapping:** The exam frequently asks which model (push vs. poll) applies to which service, and how to tune throughput with batch settings.

### 1.3 API Gateway Mapping Templates (VTL)
- [ ] **Objective:** Transform request and response payloads using Velocity Template Language.
- **Services:** API Gateway (REST), AWS Lambda
- **Steps:**
  - Create a non-proxy Lambda integration so you control the request/response mapping templates.
  - Write a request VTL template that extracts query string parameters and reshapes them into a JSON body for Lambda.
  - Write a response VTL template that wraps the Lambda result with `statusCode`, `data`, and `requestId` envelope fields.
  - Use the API Gateway **Test** console to validate templates before deploying.
- **Implementation Nuance & Trickiness:**
  - **Business Use Case & URL Headers:** Critical when integrating with legacy clients. You can use VTL to inject, override, or drop specific HTTP headers before they reach your backend, or enforce strict URL path parameter mapping.
  - **Trickiness:** VTL is notoriously hard to debug. You must rely heavily on API Gateway execution logs. Ensure CORS headers (`Access-Control-Allow-Origin`) are explicitly returned in your mock or integration responses if calling from a browser.
- **Exam Mapping:** VTL mapping templates are a classic exam topic – know when to use proxy vs. non-proxy integration.

### 1.4 DynamoDB Indexes & Query Patterns
- [ ] **Objective:** Design DynamoDB tables that **avoid full table scans**.
- **Services:** Amazon DynamoDB
- **Steps:**
  - Create a `Orders` table with PK `customerId` and SK `orderDate` (ISO-8601 string) so range queries are natural.
  - Add a **Global Secondary Index (GSI)** keyed on `status` + `orderDate` to support order-status dashboards.
  - Add a **Local Secondary Index (LSI)** keyed on `customerId` + `totalAmount` for "top spenders per customer" queries.
  - Run `Query` operations against the base table, the GSI, and the LSI – verify with `--return-consumed-capacity TOTAL` that no full scans are happening.
- **Implementation Nuance & Trickiness:**
  - **Sensitive Data & Size:** Storing PII? DynamoDB encrypts at rest, but strict compliance may require client-side encryption before writing. Also, partitions split mechanically around 10GB of data or 3000 RCU/1000 WCU.
  - **TTL & Event Triggers:** You can set a Time-to-Live (TTL) attribute to automatically expire old data. *Trickiness:* TTL deletions are free, but they *do* appear in DynamoDB Streams! You can use this "event trigger" to invoke a Lambda that archives the expired item to S3, offering the **LEAST operational overhead** for data lifecycle management.
  - **Trickiness:** GSIs are updated asynchronously. Under high throughput, if your GSI is under-provisioned, it can throttle writes to your *base* table. LSIs must be created at table creation and share the 10GB partition limit with the base table.
- **Exam Mapping:** Indexes, single-table design, and the GSI vs. LSI distinction are guaranteed exam content.

### 1.5 SNS → SQS Fan-Out
- [ ] **Objective:** Decouple producers and consumers using a publish/subscribe fan-out pattern.
- **Services:** Amazon SNS, Amazon SQS, AWS Lambda
- **Steps:**
  - Create an SNS topic `OrderEvents` and two SQS queues (`AnalyticsQueue`, `BillingQueue`), each with a dead-letter queue.
  - Subscribe both SQS queues to the topic and apply **SNS subscription filter policies** so only relevant events reach each queue.
  - Publish a test message and confirm both queues receive a copy.
  - Wire each queue to its own Lambda consumer.
- **Implementation Nuance & Trickiness:**
  - **High Volume Data:** SNS scales virtually infinitely, but downstream consumers might not. SQS acts as a shock absorber.
  - **Trickiness:** Standard SQS guarantees "at-least-once" delivery, meaning your Lambda *will* occasionally receive duplicate messages. The downstream code must be perfectly idempotent.
- **Exam Mapping:** Fan-out is the canonical decoupling pattern; the exam asks how to filter events before they fan out and how to guarantee delivery with DLQs.

### 1.6 EventBridge Custom Bus & Schedules
- [ ] **Objective:** Route custom application events using EventBridge.
- **Services:** Amazon EventBridge, AWS Lambda, Amazon SQS
- **Steps:**
  - Create a custom event bus and publish events with `PutEvents` from a sample script.
  - Write a rule with a JSON event pattern that matches `source: "myapp.orders"` and `detail-type: "OrderPlaced"` and routes to Lambda.
  - Create a second rule using a **schedule expression** (`rate(5 minutes)`) to invoke an SQS target.
  - Add a dead-letter queue and retry policy to the rule's target configuration.
- **Implementation Nuance & Trickiness:**
  - **Business Use Case:** Routing order events across completely different AWS accounts (e.g., separate billing vs. fulfillment AWS accounts).
  - **Trickiness:** EventBridge has a hard limit on payload size (256 KB). For larger data chunks, implement the "claim check" pattern: store the massive data in S3 and pass the S3 URI in the EventBridge event.
- **Exam Mapping:** EventBridge has displaced CloudWatch Events on the exam; expect questions on event patterns, schedules, and archives/replays.

### 1.7 Step Functions Orchestration
- [ ] **Objective:** Coordinate multi-step workflows without writing orchestration code.
- **Services:** AWS Step Functions, AWS Lambda, Amazon SNS
- **Steps:**
  - Create an Express workflow with a `Choice` state, parallel branches, and a `Catch` block for failure handling.
  - Use the AWS SDK service integration to publish to SNS directly from a state (no Lambda required).
  - Inspect the visual workflow execution history and download the JSON ASL definition.
  - Re-run the same workflow as a **Standard** type and note the differences in cost and execution duration limits.
- **Implementation Nuance & Trickiness:**
  - **Time Constraints & Media Orchestration:** Step Functions is the ideal orchestration engine for complex media pipelines (e.g., extracting audio from a 2-hour video, transcribing it, and generating thumbnails). A Standard workflow can pause and wait for up to 1 year, perfect for long-running transcodes or human review. Express workflows max out at 5 minutes.
  - **Trickiness:** Passing state between steps is limited to a 256 KB payload. You cannot pass raw media arrays between states; instead, pass S3 URIs (the "claim check" pattern).
- **Exam Mapping:** Step Functions appears in workflow/orchestration questions; know Standard vs. Express trade-offs.

### 1.8 AWS CLI & SDK Fundamentals
- [ ] **Objective:** Handle pagination, retries, and credential resolution programmatically.
- **Services:** AWS CLI, AWS SDK
- **Steps:**
  - Execute an AWS CLI command (e.g., `aws s3api list-objects-v2 --bucket my-bucket`) that returns a massive result set and use the `--starting-token` and `--max-items` flags for CLI pagination.
  - Write an AWS SDK script to perform the same action, explicitly handling the `NextToken` or `Marker` in a loop.
  - Implement a custom retry strategy in the SDK client configuration to use **Exponential Backoff** with jitter when facing `ThrottlingException` (HTTP 429).
  - Verify the **Default Credential Provider Chain** locally by removing hardcoded credentials and relying on `~/.aws/credentials` or environment variables.
- **Implementation Nuance & Trickiness:**
  - **Least Operational Overhead vs Custom Logic:** The SDK automatically handles basic retries (usually up to 3 times) for transient errors (like HTTP 5xx) with built-in exponential backoff. Relying on this default offers the **LEAST operational overhead**. Writing custom retry wrappers is the **MOST operational overhead** and is only necessary if overriding default limits or handling specific HTTP 4xx errors (which the SDK does not retry by default).
  - **Trickiness:** The exam heavily tests the Default Credential Provider Chain order: Environment Variables first, then local `~/.aws/credentials` (`default` profile), then ECS container credentials, and EC2 instance profiles last. If you have stale credentials in your Env Vars, they will silently override an IAM role attached to your compute instance.
- **Exam Mapping:** Exponential backoff, pagination (`NextToken`), and the exact order of the credential provider chain are guaranteed, standalone exam questions.

### 1.9 Kinesis Data Streams vs. SQS
- [ ] **Objective:** Understand the difference between real-time streaming and queuing.
- **Services:** Amazon Kinesis, Amazon SQS
- **Steps:**
  - Create a Kinesis stream with 2 shards and put records using a Partition Key.
  - Retrieve records manually using a Shard Iterator (`TRIM_HORIZON`).
- **Implementation Nuance & Trickiness:**
  - **Ordering:** Kinesis guarantees order *within a shard* based on the partition key. SQS Standard does not guarantee strict ordering.
- **Exam Mapping:** Guaranteed questions comparing Kinesis (streaming/replayable) to SQS (decoupled tasks).

### 1.10 ECS, Fargate, and ECR
- [ ] **Objective:** Build, push, and run Docker containers.
- **Services:** Amazon ECR, Amazon ECS, AWS Fargate
- **Steps:**
  - Create an ECR repository and push a Docker image using the CLI.
  - Understand the difference between an ECS Task Definition, Task, and Service.
- **Implementation Nuance & Trickiness:**
  - **IAM Roles:** The *Task Execution Role* pulls the image from ECR. The *Task Role* allows the container code to access AWS services (like DynamoDB).
- **Exam Mapping:** Core topic spanning Domains 1 and 3. Know the difference between the two IAM roles.

---

## Domain 2 – Security (26%)

### 2.1 Cognito User Pool + Identity Pool
- [ ] **Objective:** Authenticate end users and grant them temporary AWS credentials.
- **Services:** Amazon Cognito, Amazon S3, IAM
- **Steps:**
  - Create a Cognito **User Pool** with email sign-up, MFA optional, and a hosted UI domain.
  - Create a Cognito **Identity Pool** that federates the user pool and assigns an authenticated IAM role.
  - Scope the authenticated role to allow only `s3:GetObject` on `arn:aws:s3:::my-bucket/${cognito-identity.amazonaws.com:sub}/*` – per-user prefixes.
  - Sign in via the hosted UI, exchange the JWT for AWS credentials, and use them to download an object.
- **Implementation Nuance & Trickiness:**
  - **Customer Types:** B2B customers often require SAML/OIDC federation (Okta, Azure AD), whereas B2C apps use User Pools with social logins.
  - **Trickiness:** Cognito JWT tokens expire (Access/ID tokens max 1 hour). The frontend client must actively manage the refresh token flow to maintain persistent sessions without kicking the user out.
- **Exam Mapping:** The exam clearly distinguishes user pools (authentication / JWTs) from identity pools (AWS credentials). Know which is which.

### 2.2 Customer-Managed KMS Encryption
- [ ] **Objective:** Encrypt data at rest with a customer-managed key (CMK) and rotate it.
- **Services:** AWS KMS, Amazon S3, Amazon DynamoDB
- **Steps:**
  - Create a symmetric customer-managed KMS key and enable **automatic annual rotation**.
  - Apply default S3 bucket encryption with `aws:kms` and your CMK ID.
  - Create a DynamoDB table that uses the same CMK for at-rest encryption.
  - Author a key policy that grants `kms:Decrypt` only to a specific Lambda execution role – verify access works for that role and is denied for others.
- **Implementation Nuance & Trickiness:**
  - **Sensitive Data & Compliance:** Regulated industries (healthcare, finance) often dictate rotation every 90 days. AWS Managed Keys rotate every 1 year and cannot be changed, meaning Customer Managed Keys are strictly required for compliance.
  - **Trickiness:** KMS has strict request quotas. If a Lambda decrypts data 10,000 times a second, you will get throttled. Use AWS Encryption SDK Data Key Caching to reuse data keys locally.
- **Exam Mapping:** KMS key policies vs. IAM policies, key rotation, and envelope encryption are recurring exam themes.

### 2.3 Secrets Manager from Lambda
- [ ] **Objective:** Retrieve database credentials securely at runtime, never hard-coding them.
- **Services:** AWS Secrets Manager, AWS Lambda, IAM
- **Steps:**
  - Store a JSON secret containing `username`, `password`, and `host` for an RDS or DocumentDB cluster.
  - Enable **automatic rotation** with the AWS-provided rotation Lambda template.
  - In your application Lambda, call `GetSecretValue` and **cache** the result in a module-level variable to avoid excessive API calls.
  - Tighten the execution role to `secretsmanager:GetSecretValue` on a specific secret ARN only (least privilege).
- **Implementation Nuance & Trickiness:**
  - **Varying Data & Traffic:** High traffic apps retrieving secrets on every invocation will generate massive API costs and throttling.
  - **Trickiness:** Caching the secret outside the Lambda handler is mandatory, but you must implement logic to catch authentication failures (which happen when the secret rotates automatically), flush the cache, and refetch the new secret instantly.
- **Exam Mapping:** Secrets Manager vs. Parameter Store, automatic rotation, and caching strategies are common exam questions.

### 2.4 Parameter Store for Configuration
- [ ] **Objective:** Externalize non-secret configuration with hierarchical parameters.
- **Services:** AWS Systems Manager Parameter Store, AWS Lambda
- **Steps:**
  - Create parameters under a hierarchy like `/myapp/dev/featureFlag/newCheckout`.
  - Store one as a `SecureString` encrypted with a CMK; compare retrieval cost vs. Secrets Manager.
  - Use `GetParametersByPath` from a Lambda to fetch all parameters for a given environment.
  - Reference the parameter directly in a CloudFormation template using the `{{resolve:ssm:...}}` syntax.
- **Implementation Nuance & Trickiness:**
  - **Business Use Case:** Separating code from configuration allows business users or automated pipelines to toggle feature flags globally without redeploying code.
  - **Trickiness:** Standard parameters have a 4 KB size limit. For massive JSON configurations, you must upgrade to Advanced Parameters (up to 8 KB, but incurs costs).
- **Exam Mapping:** Know when to choose Parameter Store (free tier for standard, simpler) vs. Secrets Manager (rotation built in).

### 2.5 IAM Roles with Least Privilege
- [ ] **Objective:** Apply the principle of least privilege across compute services.
- **Services:** AWS IAM, Amazon EC2, AWS Lambda
- **Steps:**
  - Create an EC2 instance profile that allows only `s3:GetObject` and `s3:PutObject` on a single bucket prefix.
  - Create a separate Lambda execution role with only the actions that function actually performs (use IAM Access Analyzer policy generation as a reference).
  - Add **resource-based policy conditions** (e.g., `aws:SourceVpc`, `aws:SourceArn`) to prevent confused-deputy issues.
  - Audit both roles with IAM Access Analyzer "unused access" findings.
- **Implementation Nuance & Trickiness:**
  - **Enterprise Scale:** Managing roles for thousands of developers or apps is tricky. You transition to Attribute-Based Access Control (ABAC), tagging users and resources, allowing IAM policies to dynamically permit access if tags match.
  - **Trickiness:** Inline IAM policies have size limits (e.g., 10,240 characters for roles). If you explicitly list hundreds of ARNs, the deployment will fail. You must use wildcards strategically or consolidate resources.
- **Exam Mapping:** Roles, trust policies, and least privilege are core security topics on every iteration of the exam.

### 2.6 Pre-signed URLs for S3
- [ ] **Objective:** Grant time-limited access to private S3 objects without sharing credentials.
- **Services:** Amazon S3, AWS Lambda, AWS SDK
- **Steps:**
  - Lock down a bucket with `BlockPublicAccess` enabled and no public bucket policy.
  - Implement a Lambda function that generates a pre-signed `GetObject` URL with a 5-minute expiration.
  - Implement a separate Lambda that returns a pre-signed `PutObject` URL (allow direct browser uploads).
  - Test that the URLs stop working after expiration and that the underlying objects remain private.
- **Implementation Nuance & Trickiness:**
  - **Varying Media Types & Sizes:** Uploading a small avatar image or short audio clip via a single pre-signed URL is easy. Uploading a 50GB raw video file or a multitrack audio session requires a completely different architecture.
  - **S3 Bucket CORS & URL Headers:** When generating a pre-signed `PutObject` URL for direct browser uploads to an S3 bucket, you must configure the bucket's CORS policy to allow specific HTTP headers (like `Content-Type`). Furthermore, if you sign the URL with specific metadata headers (e.g., `x-amz-meta-userid`), the client *must* include those exact headers in their PUT request, or AWS will reject the upload.
  - **Trickiness:** For massive media files, a single pre-signed URL will time out or fail over unreliable networks. You must generate multiple pre-signed URLs to facilitate an S3 Multipart Upload, assembling them upon completion.
- **Exam Mapping:** Pre-signed URLs are a frequent exam scenario for "secure file sharing" questions.

### 2.7 API Gateway Authorizers
- [ ] **Objective:** Secure an API Gateway endpoint using Cognito or Lambda Authorizers.
- **Services:** Amazon API Gateway, Amazon Cognito, AWS Lambda
- **Steps:**
  - Configure a Cognito User Pool Authorizer in API Gateway.
  - Write a sample Lambda Custom Authorizer that returns an IAM Policy Document.
- **Implementation Nuance & Trickiness:**
  - **Cognito vs Custom:** Use Cognito if you just need to validate a JWT. Use a Lambda Custom Authorizer if you are using a 3rd party IDP (Auth0) or need complex authorization logic based on headers/body.
- **Exam Mapping:** Expect scenario questions asking you to choose the right authorizer type.

---

## Domain 3 – Deployment (24%)

### 3.1 SAM CLI End-to-End
- [ ] **Objective:** Author, build, and deploy a serverless app declaratively.
- **Services:** AWS SAM, AWS CloudFormation, AWS Lambda, API Gateway
- **Steps:**
  - Run `sam init` with the `hello-world` template and inspect the generated `template.yaml` (note `AWS::Serverless::Function`, `Globals`, `Events`).
  - Modify the template to add a DynamoDB table and an environment variable referencing the table name.
  - Run `sam build` followed by `sam deploy --guided` and accept the generated CloudFormation changeset.
  - Use `sam delete` to clean up the entire stack.
- **Implementation Nuance & Trickiness:**
  - **Enterprise Constraints:** Security teams often require a `PermissionsBoundary` to be attached to any IAM role created. SAM has global flags (`--permissions-boundary`) to handle this seamlessly.
  - **Trickiness:** SAM abstracts resources like API Gateway automatically. If you go into the AWS Console and manually tweak an API Gateway route generated by SAM, subsequent SAM deployments will likely fail due to CloudFormation drift.
- **Exam Mapping:** SAM transforms and the `AWS::Serverless::*` resource types are explicit Domain 3 content.

### 3.2 SAM Local Testing
- [ ] **Objective:** Iterate on serverless code without deploying to AWS for every change.
- **Services:** AWS SAM CLI, Docker
- **Steps:**
  - Run `sam local invoke MyFunction --event events/event.json` and verify the function executes locally.
  - Run `sam local start-api` and `curl http://127.0.0.1:3000/hello` to test the full HTTP path.
  - Use `sam local generate-event apigateway aws-proxy` to scaffold a realistic event payload.
  - Attach a debugger by passing `-d 5858` to `sam local invoke` and stepping through the handler in VS Code.
- **Implementation Nuance & Trickiness:**
  - **Data Integration:** Local testing executes compute locally but requires real AWS credentials to hit external services (DynamoDB, S3) unless you explicitly mock them or use emulators like DynamoDB Local.
  - **Trickiness:** SAM local doesn't perfectly emulate IAM. A function that works perfectly locally might immediately fail in AWS because your local machine has Admin credentials while the deployed Lambda execution role lacks permissions.
- **Exam Mapping:** Several exam questions ask which SAM CLI command does what – memorize `init`, `build`, `deploy`, `local invoke`, `local start-api`, `package`, `sync`.

### 3.3 CodeBuild buildspec.yml
- [ ] **Objective:** Compile, test, and package source code in a managed build environment.
- **Services:** AWS CodeBuild, Amazon S3, AWS CodeArtifact (optional)
- **Steps:**
  - Create a `buildspec.yml` with `install`, `pre_build`, `build`, and `post_build` phases.
  - Use the `env.parameter-store` and `env.secrets-manager` blocks to inject configuration without hard-coding.
  - Define `artifacts` so build output is uploaded to an S3 bucket.
  - Add `cache.paths` (e.g., `~/.m2/**/*` or `node_modules/**/*`) to speed up subsequent builds.
- **Implementation Nuance & Trickiness:**
  - **Varying Workloads:** Enterprise Java/C++ builds can take 30+ minutes and heavily incur compute costs.
  - **Trickiness:** Not caching dependencies (like `node_modules` or `.m2`) will double your build time and cost. CodeBuild caches to S3, but local caching offers even faster retrieval for massive projects.
- **Exam Mapping:** Phase order, the `env` block, and cache configuration in buildspec files are common questions.

### 3.4 CodeDeploy appspec.yml on EC2
- [ ] **Objective:** Automate application deployments to EC2 with lifecycle hooks.
- **Services:** AWS CodeDeploy, Amazon EC2, IAM
- **Steps:**
  - Install the CodeDeploy agent on a tagged EC2 instance and create a deployment group targeting that tag.
  - Author an `appspec.yml` with `BeforeInstall`, `AfterInstall`, `ApplicationStart`, and `ValidateService` hooks.
  - Each hook runs a small shell script (e.g., stop service, copy files, start service, run smoke test).
  - Trigger a deployment from a zipped revision in S3 and watch the lifecycle events in the console.
- **Implementation Nuance & Trickiness:**
  - **Varying Capacity:** Handling deployments across an Auto Scaling Group (ASG) that is constantly shifting size.
  - **Trickiness:** If a scale-out event happens *during* a deployment, CodeDeploy automatically pauses the scale-out, pushes the last successful revision to the new instance, and then attaches it to the load balancer, ensuring consistency.
- **Exam Mapping:** Hook order and the difference between EC2/On-Premises, Lambda, and ECS appspec formats are frequently tested.

### 3.5 Blue/Green & Canary with Lambda Aliases
- [ ] **Objective:** Shift traffic safely between Lambda versions.
- **Services:** AWS Lambda, AWS CodeDeploy, Amazon API Gateway
- **Steps:**
  - Publish a new Lambda version and create an alias `live` pointing at it.
  - Configure a CodeDeploy deployment group with `LambdaCanary10Percent5Minutes` for traffic shifting.
  - Add a CloudWatch Alarm as the **rollback trigger** if errors exceed a threshold during the canary window.
  - Compare with API Gateway **canary stage settings** for splitting traffic at the API layer.
- **Implementation Nuance & Trickiness:**
  - **Business Use Case:** Zero-downtime deployments for high-availability SaaS platforms.
  - **Trickiness:** Database schema changes are notoriously difficult with Canary deployments. Because V1 and V2 of your app are running simultaneously for 5 minutes, database additions must be strictly backward compatible.
- **Exam Mapping:** All-at-once, linear, and canary deployment configurations are explicit exam vocabulary.

### 3.6 CodePipeline End-to-End
- [ ] **Objective:** Build a Source → Build → Deploy pipeline.
- **Services:** AWS CodePipeline, AWS CodeBuild, AWS CodeDeploy, GitHub or AWS CodeCommit
- **Steps:**
  - Create a pipeline with three stages: Source (Git), Build (CodeBuild using your `buildspec.yml`), and Deploy (CodeDeploy or CloudFormation).
  - Add a **manual approval** action between Build and Deploy.
  - Encrypt the pipeline's S3 artifact bucket with a customer-managed KMS key.
  - Trigger a pipeline run by pushing a commit and watch each stage transition.
- **Implementation Nuance & Trickiness:**
  - **Enterprise Security:** Organizations rarely put Dev, QA, and Prod pipelines in the same account.
  - **Trickiness:** Cross-account CodePipeline deployments require highly complex IAM trust relationships and a shared S3 bucket encrypted with a Customer-Managed KMS key. Default AWS managed keys (`aws/s3`) will not work across accounts.
- **Exam Mapping:** Pipeline structure, approval actions, and artifact encryption show up regularly.

### 3.7 CloudFormation Drift & Change Sets
- [ ] **Objective:** Manage infrastructure changes safely.
- **Services:** AWS CloudFormation
- **Steps:**
  - Deploy a stack from a template, then manually modify a resource (e.g., add a tag in the console).
  - Run a **drift detection** and review the drifted resources.
  - Modify the template and create a **change set** before executing it – inspect what will change.
  - Use `DeletionPolicy: Retain` and `UpdateReplacePolicy` on a stateful resource (e.g., a DynamoDB table).
- **Implementation Nuance & Trickiness:**
  - **Sensitive Data & State:** Modifying stateful resources (DynamoDB, RDS) without extreme caution.
  - **Trickiness:** Simply changing the physical `TableName` property in CloudFormation will cause a "Replacement" event. The old table is deleted, the new one is created. If `DeletionPolicy: Retain` is not set, all production data is instantly wiped out.
- **Exam Mapping:** Change sets, drift, deletion policies, and intrinsic functions (`!Ref`, `!Sub`, `!GetAtt`) are heavily tested.

### 3.8 Elastic Beanstalk & .ebextensions
- [ ] **Objective:** Deploy an application and modify its environment using `.ebextensions`.
- **Services:** AWS Elastic Beanstalk
- **Steps:**
  - Initialize an application with `eb init` and deploy with `eb create`.
  - Create a `.ebextensions/` folder to set environment variables and install packages.
- **Implementation Nuance & Trickiness:**
  - **Deployment Policies:** Immutable deployments spin up a temporary Auto Scaling Group and are the safest. All-at-once is fastest but causes downtime.
- **Exam Mapping:** Knowing deployment policies and the purpose of `.ebextensions` vs saved configurations is heavily tested.

---

## Domain 4 – Troubleshooting and Optimization (18%)

### 4.1 X-Ray Distributed Tracing
- [ ] **Objective:** Trace a request across multiple services to find latency bottlenecks.
- **Services:** AWS X-Ray, AWS Lambda, Amazon API Gateway, Amazon DynamoDB
- **Steps:**
  - Enable **active tracing** on both API Gateway and Lambda.
  - Instrument a Lambda function with the X-Ray SDK; wrap the AWS SDK so DynamoDB calls show up as subsegments.
  - Add **annotations** (filterable, indexed) for `customerId` and **metadata** (not indexed) for the full request payload.
  - Open the X-Ray service map and identify the slowest hop using the trace timeline.
- **Implementation Nuance & Trickiness:**
  - **High Volume Data:** Tracing 100,000 requests a second is exorbitantly expensive and mostly useless noise.
  - **Trickiness:** You must configure X-Ray Sampling Rules (e.g., 1 request per second, then 5% of remaining requests) to get statistical visibility without blowing up your cloud bill.
- **Exam Mapping:** Annotations vs. metadata, sampling rules, and the X-Ray daemon are common exam content.

### 4.2 CloudWatch Logs Insights & Embedded Metric Format
- [ ] **Objective:** Turn structured logs into queryable metrics without instrumentation overhead.
- **Services:** Amazon CloudWatch Logs, CloudWatch Metrics
- **Steps:**
  - In a Lambda function, emit a log line in **EMF** format that contains a custom metric (e.g., `OrderTotal`).
  - Confirm the metric appears under the namespace you specified – no `PutMetricData` API call required.
  - Write a Logs Insights query: `fields @timestamp, @message | filter level = "ERROR" | stats count() by bin(5m)`.
  - Save the query and pin it to a CloudWatch dashboard.
- **Implementation Nuance & Trickiness:**
  - **Varying Amounts of Data:** Logging heavy JSON blobs at massive scale incurs hefty ingestion charges.
  - **Trickiness:** Using synchronous `PutMetricData` API calls inside Lambda blocks execution and adds latency. EMF parses logs asynchronously, eliminating latency impact, but high cardinality dimensions (e.g., `customerId` for a million users) will result in massive Custom Metric costs.
- **Exam Mapping:** EMF, metric filters, and Logs Insights queries are increasingly featured on the current exam blueprint.

### 4.3 CloudWatch Alarms & Composite Alarms
- [ ] **Objective:** Alert proactively on operational issues.
- **Services:** Amazon CloudWatch, Amazon SNS
- **Steps:**
  - Create a metric alarm on Lambda `Errors > 5` over 5 minutes that publishes to an SNS topic.
  - Create a second alarm on `Throttles` for the same function.
  - Combine both into a **composite alarm** with the rule `ALARM(errors) AND ALARM(throttles)`.
  - Subscribe an email endpoint and trigger the alarm by intentionally erroring out the function.
- **Implementation Nuance & Trickiness:**
  - **Business Use Case:** Preventing "alert fatigue" during highly variable traffic periods (e.g., Black Friday).
  - **Trickiness:** Hard-coded thresholds fail when traffic naturally surges. Using CloudWatch Anomaly Detection models evaluates historical trends and only fires when errors deviate from the *expected* baseline.
- **Exam Mapping:** Alarm states, evaluation periods, and treat-missing-data settings come up frequently.

### 4.4 DAX vs. ElastiCache for DynamoDB
- [ ] **Objective:** Reduce read latency on hot data.
- **Services:** Amazon DynamoDB Accelerator (DAX), Amazon ElastiCache (Redis)
- **Steps:**
  - Create a DAX cluster in your VPC and update your application to use the **DAX client** instead of the standard DynamoDB client.
  - Compare `GetItem` latency before and after using CloudWatch metrics.
  - As an alternative, deploy a single-node ElastiCache Redis cluster and implement the **cache-aside** pattern in code.
  - Document when each choice is appropriate (DAX = transparent, DynamoDB-only; ElastiCache = generic, multi-source).
- **Implementation Nuance & Trickiness:**
  - **Operational Overhead (Least vs Most):** DAX requires zero application code changes (just swap the DynamoDB SDK client), offering the **LEAST operational overhead**. ElastiCache (Redis) requires writing custom "cache-aside" logic in your application code, representing the **MOST operational overhead**.
  - **Redis & TTL Stuff:** When using Redis, you must explicitly write code to set a TTL (Time-To-Live) on every key to prevent memory exhaustion and manage stale data. DAX handles item caching natively.
  - **Trickiness:** If your app runs a massive `Scan` or `Query` on the database, DAX will dutifully cache the entire result set, potentially evicting the actually useful "hot" data from memory. DAX is best strictly for high-volume `GetItem` requests.
- **Exam Mapping:** The exam often presents a "high read traffic on DynamoDB" scenario – know that DAX is the DynamoDB-specific answer.

### 4.5 Lambda Performance Tuning
- [ ] **Objective:** Find the right memory/timeout sweet spot for cost and latency.
- **Services:** AWS Lambda, AWS Lambda Power Tuning, Amazon CloudWatch
- **Steps:**
  - Deploy the open-source **Lambda Power Tuning** state machine and run it against a representative function.
  - Compare runtime/cost graphs at 128 MB, 512 MB, 1024 MB, and 1769 MB (1 vCPU break-even).
  - Enable **Provisioned Concurrency** to mitigate cold starts on a latency-sensitive alias.
  - Reduce the deployment package size by trimming dependencies and using Lambda layers for shared libraries.
- **Implementation Nuance & Trickiness:**
  - **Time Constraints:** A customer-facing API needs sub-200ms response times.
  - **Trickiness:** Memory settings linearly control CPU and network throughput. Bumping a Lambda from 128MB to 1024MB often makes it execute 10x faster, resulting in a *lower* overall bill. Also, Provisioned Concurrency eliminates cold starts but charges you continuously even when idle.
- **Exam Mapping:** Cold starts, provisioned concurrency, and memory tuning are common Domain 4 questions.

### 4.6 API Gateway Throttling, Caching, and Usage Plans
- [ ] **Objective:** Protect downstream services and improve response time at the edge.
- **Services:** Amazon API Gateway
- **Steps:**
  - Configure **stage-level throttling** (rate + burst) for the `dev` stage.
  - Enable response caching on a `GET /items/{id}` resource and verify cache hits in CloudWatch metrics.
  - Create an API key + usage plan that limits a partner to 1,000 requests/day.
  - Test 429 (`Too Many Requests`) responses by exceeding the limit with a load tool.
- **Implementation Nuance & Trickiness:**
  - **Customer Types:** A SaaS platform offering Free, Pro, and Enterprise tiers.
  - **Trickiness:** Stage-level limits apply globally across the API. To offer tiered limits (e.g., Free = 10 req/s, Enterprise = 1000 req/s), you must extract API Keys from the headers, associate them with Usage Plans, and enforce throttling dynamically per tenant.
- **Exam Mapping:** Throttling, caching, and usage plans are explicit DVA-C02 objectives.

---

## Bonus – Supplementary Services

### B.1 Amazon Athena: Query S3 Data with SQL
- [ ] **Objective:** Query structured data in S3 directly using standard SQL.
- **Services:** Amazon Athena, Amazon S3, AWS Glue
- **Steps:**
  - Create an external table over CSV data in S3.
  - Use CTAS (Create Table As Select) to partition the data and convert it to Parquet format.
- **Implementation Nuance & Trickiness:**
  - **Cost Optimization:** Using `LIMIT 10` does *not* reduce the amount of data scanned. To lower costs, you must partition the data and use columnar formats like Parquet/ORC.
- **Exam Mapping:** Often the correct answer for "how to run ad-hoc queries on serverless S3 logs/data."

---

## Capstone Project – "Serverless Order Platform"

Combine **at least nine** of the services you practiced above into one CloudFormation/SAM-deployed application, injecting real-world data and security constraints.

**High-level architecture & Constraints:**

1. **Cognito User Pool:** Authenticates B2C and B2B customers. Ensure token validity and implement refresh token handling for persistent sessions.
2. **API Gateway (REST):** Exposes `POST /orders` and `GET /orders/{id}`. Implement **Usage Plans** to throttle the free tier to 100 req/min while giving the Enterprise tier 5000 req/min.
3. **Lambda & DynamoDB:** The `POST` Lambda writes to `Orders` (on-demand capacity). **Trickiness:** Implement client-side encryption for the customer's PII (address/phone) *before* writing to DynamoDB, alongside KMS at-rest encryption.
4. **DynamoDB Streams & SNS:** Trigger a `PublishOrderEvent` Lambda that fans out to SNS. 
5. **SQS Fan-Out:** Two SQS queues (`BillingQueue`, `AnalyticsQueue`) subscribe to SNS. Ensure the Billing Lambda implements **idempotency checks** (tracking processed `messageId`s) to handle SQS's at-least-once delivery duplicates.
6. **EventBridge Scheduler:** Runs a nightly reconciliation. Must handle massive order sets by pulling data iteratively (handling 1MB payload limits).
7. **Secrets Manager:** Stores payment credentials. The Billing Lambda must fetch and **cache** this secret globally, including fallback logic to flush the cache if auth fails due to a key rotation.
8. **Large Media Handling (Images/Audio/Video):** Orders containing massive 4K video assets, uncompressed audio stems, or high-res image catalogs (> 100MB) bypass API Gateway. Generate **Multipart S3 Pre-signed URLs** to let the browser upload directly to S3, which then triggers an asynchronous Lambda to generate image thumbnails and low-bitrate audio/video previews.
9. **X-Ray & CloudWatch:** Enable X-Ray with a **5% sampling rule** to prevent exorbitant tracing costs. Set up a CloudWatch **Composite Alarm** to only alert you if Error Rates *and* Latency both spike.
10. **CI/CD:** Use CodePipeline. Ensure any database schema updates via CloudFormation strictly use `DeletionPolicy: Retain` to prevent catastrophic data loss during drift or rollbacks.

**Acceptance criteria:**
- [ ] All resources are defined in a single SAM template (no console clicks beyond stack creation).
- [ ] No hard-coded secrets anywhere – everything resolves via Secrets Manager or Parameter Store.
- [ ] A failed payment triggers the SQS DLQ and a CloudWatch alarm fires.
- [ ] An X-Ray service map shows the full path from API Gateway → Lambda → DynamoDB → SNS → SQS → Lambda.
- [ ] A code change pushed to `main` deploys safely via canary and can roll back automatically.
- [ ] Total monthly cost in idle state is below $5 (Free Tier friendly).

Completing this capstone exercises every Domain 1–4 objective and is the single best preparation activity for the DVA-C02 exam, combining rote knowledge with critical architectural thinking.

---

## Study Tips

- After each lab, write a **2-sentence summary** in your own words – retrieval practice is more effective than re-reading docs.
- Bookmark the official [DVA-C02 Exam Guide](https://aws.amazon.com/certification/certified-developer-associate/) and check off each task statement as you cover it.
- Take at least two full-length practice exams in the final week; review every wrong answer until you can explain *why* the correct option is correct.
- Tear down resources nightly with `sam delete` or `aws cloudformation delete-stack` to keep the bill near zero.

Good luck, Curtis – you've got this.
