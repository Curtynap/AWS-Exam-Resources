"""
DVA-C02 Task 1.2 — SQS Message Processor (POLL Model)

This Lambda is invoked by the Lambda service which POLLS the SQS queue.
This is the POLL invocation model using an event source mapping.

EXAM TIP: SQS event source mappings use long-polling.
Lambda deletes messages ONLY after your handler returns successfully.
If your handler throws an exception, the entire batch becomes visible
again after the VisibilityTimeout expires.
"""

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Process SQS messages with partial batch failure reporting.
    
    EXAM TIP: With ReportBatchItemFailures enabled, you can return a list
    of failed message IDs. Only those messages will be retried.
    Without it, ANY failure retries the ENTIRE batch (causing duplicates).
    
    The response format for partial failures:
    {
        "batchItemFailures": [
            {"itemIdentifier": "messageId1"},
            {"itemIdentifier": "messageId2"}
        ]
    }
    """
    logger.info(f"Received {len(event['Records'])} SQS message(s)")
    
    batch_item_failures = []
    
    for record in event['Records']:
        message_id = record['messageId']
        receipt_handle = record['receiptHandle']
        
        try:
            # Parse the message body
            body = json.loads(record['body'])
            logger.info(f"Processing message {message_id}: {json.dumps(body)}")
            
            # EXAM TIP: Your processing code MUST be idempotent!
            # SQS Standard queues guarantee "at-least-once" delivery.
            # Your Lambda WILL receive duplicate messages occasionally.
            # 
            # Idempotency strategies:
            # 1. Use the messageId as a deduplication key in DynamoDB
            # 2. Use SQS FIFO queues (exactly-once processing, lower throughput)
            # 3. Use the AWS Lambda Powertools idempotency decorator
            
            # Simulate processing
            order_id = body.get('orderId', 'unknown')
            amount = body.get('amount', 0)
            
            logger.info(f"Processed order {order_id} for ${amount}")
            
            # EXAM TIP: Check remaining time before processing each message.
            # If running low on time, stop processing and let remaining messages
            # become visible again via the VisibilityTimeout.
            remaining_time_ms = context.get_remaining_time_in_millis()
            if remaining_time_ms < 5000:  # Less than 5 seconds left
                logger.warning(f"Running low on time ({remaining_time_ms}ms left), stopping batch")
                # Add remaining unprocessed messages to failures
                batch_item_failures.append({'itemIdentifier': message_id})
                
        except Exception as e:
            logger.error(f"Failed to process message {message_id}: {str(e)}")
            # EXAM TIP: Add the failed message ID to batchItemFailures.
            # This message will be retried; successfully processed messages won't be.
            batch_item_failures.append({'itemIdentifier': message_id})
    
    # Return partial batch failures
    # EXAM TIP: If batchItemFailures is empty, ALL messages are deleted from SQS.
    # If it contains message IDs, only those messages are returned to the queue.
    result = {'batchItemFailures': batch_item_failures}
    
    if batch_item_failures:
        logger.warning(f"Partial failures: {len(batch_item_failures)} message(s) will be retried")
    else:
        logger.info(f"All {len(event['Records'])} message(s) processed successfully")
    
    return result
