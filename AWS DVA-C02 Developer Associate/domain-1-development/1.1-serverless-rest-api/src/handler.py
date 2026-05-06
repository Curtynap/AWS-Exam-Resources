"""
DVA-C02 Task 1.1 — Lambda CRUD Handler for Items API

This function handles all CRUD operations for the Items REST API.
It uses Lambda proxy integration, meaning:
  - The FULL HTTP request is passed in as the `event` parameter
  - We MUST return a dict with `statusCode`, `body`, and `headers`

EXAM TIP: Lambda proxy integration is the most common pattern.
The function is responsible for routing by HTTP method and path.
"""

import json
import os
import uuid
import logging
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

# ──────────────────────────────────────────────
# Setup — runs ONCE during cold start (exam: init phase)
# ──────────────────────────────────────────────
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# EXAM TIP: Initialize SDK clients OUTSIDE the handler.
# This code runs during the cold start "init phase" and is reused
# across warm invocations, saving time and money.
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


# ──────────────────────────────────────────────
# Helper — build a standard API Gateway response
# ──────────────────────────────────────────────
def build_response(status_code, body):
    """
    EXAM TIP: Lambda proxy integration REQUIRES this exact response format.
    Missing `statusCode` or `body` will cause a 502 Bad Gateway error.
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',        # CORS for browser clients
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        },
        'body': json.dumps(body, default=str)          # default=str handles datetime serialization
    }


# ──────────────────────────────────────────────
# CRUD Operations
# ──────────────────────────────────────────────
def create_item(event):
    """POST /items — Create a new item in DynamoDB."""
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return build_response(400, {'error': 'Invalid JSON in request body'})

    if not body.get('name'):
        return build_response(400, {'error': 'Field "name" is required'})

    item = {
        'itemId': str(uuid.uuid4()),               # Generate a unique ID
        'name': body['name'],
        'price': body.get('price', 0),
        'category': body.get('category', 'general'),
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'updatedAt': datetime.now(timezone.utc).isoformat(),
    }

    # EXAM TIP: PutItem is an "upsert" — it will overwrite if the key exists.
    # To prevent overwrites, add a ConditionExpression:
    #   ConditionExpression='attribute_not_exists(itemId)'
    table.put_item(Item=item)
    logger.info(f"Created item: {item['itemId']}")

    return build_response(201, {'message': 'Item created', 'item': item})


def get_item(event):
    """GET /items/{id} — Retrieve a single item by ID."""
    item_id = event['pathParameters']['id']

    # EXAM TIP: GetItem uses the partition key for a direct O(1) lookup.
    # This is the most efficient read pattern in DynamoDB.
    response = table.get_item(Key={'itemId': item_id})
    item = response.get('Item')

    if not item:
        return build_response(404, {'error': f'Item {item_id} not found'})

    return build_response(200, item)


def get_all_items(event):
    """GET /items — List all items (uses Scan — avoid in production!)."""
    # EXAM TIP: Scan reads EVERY item in the table. It's expensive and slow.
    # In production, use Query with a known partition key instead.
    # We use Scan here for simplicity in a study exercise.
    response = table.scan()
    items = response.get('Items', [])

    # EXAM TIP: Scan returns max 1MB per call. For larger datasets,
    # you must handle pagination with LastEvaluatedKey:
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items', []))

    return build_response(200, {'items': items, 'count': len(items)})


def update_item(event):
    """PUT /items/{id} — Update an existing item."""
    item_id = event['pathParameters']['id']

    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return build_response(400, {'error': 'Invalid JSON in request body'})

    if not body:
        return build_response(400, {'error': 'Request body cannot be empty'})

    # EXAM TIP: UpdateItem with UpdateExpression is more efficient than
    # PutItem because it only modifies specified attributes, not the entire item.
    # It also supports atomic counters: SET viewCount = viewCount + :inc
    update_expression_parts = []
    expression_values = {}
    expression_names = {}

    for key, value in body.items():
        if key == 'itemId':
            continue  # Don't allow changing the partition key
        safe_key = f'#{key}'
        safe_val = f':{key}'
        update_expression_parts.append(f'{safe_key} = {safe_val}')
        expression_values[safe_val] = value
        expression_names[safe_key] = key

    # Always update the timestamp
    update_expression_parts.append('#updatedAt = :updatedAt')
    expression_values[':updatedAt'] = datetime.now(timezone.utc).isoformat()
    expression_names['#updatedAt'] = 'updatedAt'

    try:
        response = table.update_item(
            Key={'itemId': item_id},
            UpdateExpression='SET ' + ', '.join(update_expression_parts),
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names,
            ConditionExpression='attribute_exists(itemId)',  # Fail if item doesn't exist
            ReturnValues='ALL_NEW'
        )
        return build_response(200, {
            'message': 'Item updated',
            'item': response['Attributes']
        })
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return build_response(404, {'error': f'Item {item_id} not found'})
        raise


def delete_item(event):
    """DELETE /items/{id} — Remove an item."""
    item_id = event['pathParameters']['id']

    # EXAM TIP: DeleteItem with ConditionExpression ensures we only delete
    # items that exist, and ReturnValues gives us the deleted item data.
    try:
        response = table.delete_item(
            Key={'itemId': item_id},
            ConditionExpression='attribute_exists(itemId)',
            ReturnValues='ALL_OLD'
        )
        return build_response(200, {
            'message': 'Item deleted',
            'item': response.get('Attributes', {})
        })
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return build_response(404, {'error': f'Item {item_id} not found'})
        raise


# ──────────────────────────────────────────────
# Main Handler — routes by HTTP method
# ──────────────────────────────────────────────
def lambda_handler(event, context):
    """
    EXAM TIP: With Lambda proxy integration, the event contains the
    full HTTP request including: httpMethod, path, pathParameters,
    queryStringParameters, headers, and body.

    The context object provides: function_name, memory_limit_in_mb,
    aws_request_id, and remaining time (context.get_remaining_time_in_millis()).
    """
    logger.info(f"Received event: {json.dumps(event)}")

    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    has_path_param = event.get('pathParameters') is not None

    try:
        if path == '/items' and http_method == 'GET':
            return get_all_items(event)
        elif path == '/items' and http_method == 'POST':
            return create_item(event)
        elif has_path_param and http_method == 'GET':
            return get_item(event)
        elif has_path_param and http_method == 'PUT':
            return update_item(event)
        elif has_path_param and http_method == 'DELETE':
            return delete_item(event)
        else:
            return build_response(405, {'error': f'Method {http_method} not allowed on {path}'})
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return build_response(500, {'error': 'Internal server error'})
