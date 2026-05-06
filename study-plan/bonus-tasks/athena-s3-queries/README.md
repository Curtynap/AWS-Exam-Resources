# Bonus Task — Amazon Athena: Query S3 Data with SQL

> **Time Estimate:** 1-2 hours | **Cost:** $5 per TB scanned (tiny datasets = pennies)

---

## 🎯 What You'll Learn

- Querying structured data in S3 using standard SQL (serverless, no infrastructure)
- Creating Athena databases and tables (Glue Data Catalog)
- Partitioning for cost optimization
- Integrating Athena with Lambda and API Gateway
- CTAS (Create Table As Select) for materialized results

---

## 🏗️ Architecture

```
┌──────────────┐      ┌────────────────┐      ┌──────────────┐
│  S3 Bucket   │ ───→ │  Athena        │ ───→ │  Results in  │
│  (CSV/JSON/  │      │  (SQL Engine)  │      │  S3 bucket   │
│   Parquet)   │      │                │      │              │
└──────────────┘      └────────────────┘      └──────────────┘
                            │
                      ┌─────┴─────┐
                      │ Glue Data │
                      │ Catalog   │
                      │ (Schema)  │
                      └───────────┘
```

---

## 🚀 Step-by-Step Instructions

### Step 1: Create Sample Data in S3

```bash
# Create a bucket for your data
aws s3 mb s3://dva-athena-data-YOUR_ACCOUNT_ID --region us-east-1

# Create a results bucket (Athena writes query results here)
aws s3 mb s3://dva-athena-results-YOUR_ACCOUNT_ID --region us-east-1

# Create sample order data as CSV
cat > orders.csv << 'EOF'
order_id,customer_id,order_date,amount,status,category
ORD-001,CUST-001,2026-01-15,49.99,DELIVERED,electronics
ORD-002,CUST-002,2026-01-20,149.99,SHIPPED,books
ORD-003,CUST-001,2026-02-10,24.99,DELIVERED,electronics
ORD-004,CUST-003,2026-02-14,299.99,PENDING,electronics
ORD-005,CUST-002,2026-03-01,79.99,DELIVERED,clothing
ORD-006,CUST-001,2026-03-15,199.99,SHIPPED,electronics
ORD-007,CUST-004,2026-04-01,59.99,DELIVERED,books
ORD-008,CUST-003,2026-04-10,349.99,DELIVERED,electronics
ORD-009,CUST-002,2026-05-01,89.99,PENDING,clothing
ORD-010,CUST-001,2026-05-05,129.99,SHIPPED,books
EOF

# Upload to S3 in a "folder" structure
aws s3 cp orders.csv s3://dva-athena-data-YOUR_ACCOUNT_ID/orders/orders.csv
```

### Step 2: Create a Database and Table in Athena

```bash
# Set the output location first
aws athena start-query-execution \
  --query-string "CREATE DATABASE IF NOT EXISTS dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"
```

Now create the table:
```bash
aws athena start-query-execution \
  --query-string "
    CREATE EXTERNAL TABLE IF NOT EXISTS dva_study.orders (
      order_id STRING,
      customer_id STRING,
      order_date DATE,
      amount DOUBLE,
      status STRING,
      category STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    LOCATION 's3://dva-athena-data-YOUR_ACCOUNT_ID/orders/'
    TBLPROPERTIES ('skip.header.line.count'='1')
  " \
  --query-execution-context "Database=dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"
```

### Step 3: Run SQL Queries

```bash
# Total revenue by category
aws athena start-query-execution \
  --query-string "
    SELECT category, 
           COUNT(*) as order_count, 
           ROUND(SUM(amount), 2) as total_revenue,
           ROUND(AVG(amount), 2) as avg_order_value
    FROM dva_study.orders 
    GROUP BY category 
    ORDER BY total_revenue DESC
  " \
  --query-execution-context "Database=dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"

# Get the query execution ID from the output, then fetch results:
aws athena get-query-results --query-execution-id YOUR_EXECUTION_ID
```

```bash
# Top customers
aws athena start-query-execution \
  --query-string "
    SELECT customer_id, 
           COUNT(*) as orders, 
           ROUND(SUM(amount), 2) as total_spent
    FROM dva_study.orders 
    GROUP BY customer_id 
    ORDER BY total_spent DESC
  " \
  --query-execution-context "Database=dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"
```

### Step 4: Use Partitioning for Cost Optimization

```bash
# Create a partitioned table (partitions reduce data scanned = lower cost)
aws athena start-query-execution \
  --query-string "
    CREATE TABLE dva_study.orders_partitioned
    WITH (
      format = 'PARQUET',
      external_location = 's3://dva-athena-data-YOUR_ACCOUNT_ID/orders-partitioned/',
      partitioned_by = ARRAY['status']
    ) AS
    SELECT order_id, customer_id, order_date, amount, category, status
    FROM dva_study.orders
  " \
  --query-execution-context "Database=dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"
```

### Step 5: Query from Lambda (Programmatic Access)

```python
# athena_query.py — Lambda function that queries Athena
import boto3
import time

athena = boto3.client('athena')

def lambda_handler(event, context):
    query = """
        SELECT customer_id, SUM(amount) as total
        FROM dva_study.orders
        WHERE status = 'DELIVERED'
        GROUP BY customer_id
    """
    
    # Start the query (async)
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'dva_study'},
        ResultConfiguration={
            'OutputLocation': 's3://dva-athena-results-YOUR_ACCOUNT_ID/'
        }
    )
    execution_id = response['QueryExecutionId']
    
    # Poll for completion
    while True:
        result = athena.get_query_execution(QueryExecutionId=execution_id)
        state = result['QueryExecution']['Status']['State']
        if state in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
            break
        time.sleep(1)
    
    if state == 'SUCCEEDED':
        results = athena.get_query_results(QueryExecutionId=execution_id)
        return {'statusCode': 200, 'body': str(results['ResultSet']['Rows'])}
    else:
        return {'statusCode': 500, 'body': f'Query {state}'}
```

---

## 🧠 Exam-Critical Concepts

### When to Use Athena

| Scenario | Best Service |
|----------|-------------|
| Ad-hoc SQL queries on S3 data | **Athena** |
| Real-time queries on DynamoDB | DynamoDB / DAX |
| Complex ETL transformations | Glue |
| Dashboard analytics | Athena + QuickSight |
| Log analysis (CloudWatch) | Logs Insights |

### Cost Optimization Strategies

| Strategy | Impact |
|----------|--------|
| **Columnar format (Parquet/ORC)** | 30-90% less data scanned |
| **Partitioning** | Skip irrelevant data entirely |
| **Compression (Snappy, GZIP)** | Smaller files = less scanned |
| **LIMIT clause** | Still scans full data (doesn't save cost!) |

> ⚠️ **Exam Gotcha:** `LIMIT 10` does NOT reduce the amount of data scanned. Athena reads the full dataset and then limits the result. Only partitioning and columnar formats reduce costs.

### Athena + Glue Data Catalog
- Athena uses the **Glue Data Catalog** as its metastore
- Tables created in Athena are visible in Glue (and vice versa)
- Glue Crawlers can auto-discover schema from S3 data

### Federated Queries
- Athena can query across **DynamoDB**, **RDS**, **Redshift**, and other sources using Lambda-based connectors
- Useful for cross-service analytics without ETL

---

## 🧹 Teardown

```bash
# Drop tables and database
aws athena start-query-execution \
  --query-string "DROP TABLE IF EXISTS dva_study.orders_partitioned" \
  --query-execution-context "Database=dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"

aws athena start-query-execution \
  --query-string "DROP TABLE IF EXISTS dva_study.orders" \
  --query-execution-context "Database=dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"

aws athena start-query-execution \
  --query-string "DROP DATABASE IF EXISTS dva_study" \
  --result-configuration "OutputLocation=s3://dva-athena-results-YOUR_ACCOUNT_ID/"

# Delete S3 data
aws s3 rm s3://dva-athena-data-YOUR_ACCOUNT_ID --recursive
aws s3 rb s3://dva-athena-data-YOUR_ACCOUNT_ID
aws s3 rm s3://dva-athena-results-YOUR_ACCOUNT_ID --recursive
aws s3 rb s3://dva-athena-results-YOUR_ACCOUNT_ID
```

---

## ✅ Completion Checklist

- [ ] Created sample CSV data in S3
- [ ] Created Athena database and table via SQL
- [ ] Ran aggregation queries (revenue by category, top customers)
- [ ] Created a partitioned table in Parquet format (CTAS)
- [ ] Queried Athena from Lambda programmatically
- [ ] Understand why LIMIT doesn't save cost but partitioning does
- [ ] Understand Athena ↔ Glue Data Catalog relationship
- [ ] Resources torn down

---

## 📝 My Summary (Fill In After Completing)

**Date completed:**
**Key takeaway (2 sentences):**
>

**Tricky thing I learned:**
>

**Exam-relevant fact I'll remember:**
>
