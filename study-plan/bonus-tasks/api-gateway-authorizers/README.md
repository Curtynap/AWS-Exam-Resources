# Bonus Task — API Gateway Authorizers

> **Exam Weight:** Domain 2 (Security)
> **Time Estimate:** 1-2 hours | **Cost:** Free Tier

---

## 🎯 What You'll Learn

- Securing API Gateway endpoints
- Cognito User Pool Authorizers
- Lambda Custom Authorizers (Token vs. Request)
- IAM Policies for API access

---

## 🧠 Exam-Critical: Choosing an Authorizer

| Authorizer Type | When to Use It | How it Works |
|-----------------|----------------|--------------|
| **Cognito User Pool** | You use Cognito for auth, need JWT validation | API GW validates the JWT token automatically. No custom code needed. |
| **Lambda Custom (Token)** | You use a 3rd party IDP (Auth0, Okta) or custom tokens | Lambda inspects a Bearer token and returns an IAM policy allowing/denying access. |
| **Lambda Custom (Request)** | You need to authorize based on Headers, Query Params, or Body | Lambda inspects full request parameters and returns an IAM policy. |
| **IAM Authorization** | Service-to-service communication (e.g., Lambda calling API GW) | Request must be signed with AWS Signature V4 using AWS credentials. |

---

## 🚀 Key Steps

### Step 1: Lambda Custom Authorizer Code

If you choose a Lambda Custom Authorizer, this is what the code looks like. It MUST return a valid IAM policy.

```python
def lambda_handler(event, context):
    # event['authorizationToken'] contains "Bearer <token>"
    token = event.get('authorizationToken')
    
    if token == 'Bearer allow-secret-123':
        effect = 'Allow'
    elif token == 'Bearer deny-secret-123':
        effect = 'Deny'
    else:
        raise Exception('Unauthorized') # Returns 401
        
    # Build and return the IAM policy
    return {
        'principalId': 'user|a1b2c3',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': event['methodArn'] # The API endpoint being called
            }]
        },
        'context': {
            'customData': 'This context is passed to the backend Lambda'
        }
    }
```

### Step 2: SAM Template Configuration

To attach a Cognito User Pool Authorizer in SAM:

```yaml
Resources:
  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: dev
      Auth:
        DefaultAuthorizer: MyCognitoAuthorizer
        Authorizers:
          MyCognitoAuthorizer:
            UserPoolArn: !GetAtt MyUserPool.Arn

  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      # ...
      Events:
        GetApi:
          Type: Api
          Properties:
            RestApiId: !Ref MyApi
            Path: /secure-data
            Method: GET
```

---

## ✅ Completion Checklist

- [ ] Understand the 4 types of API Gateway Authorizers
- [ ] Understand that Lambda Authorizers must return an IAM Policy Document
- [ ] Understand how to configure a Cognito Authorizer in SAM
