"""
DVA-C02 Task 1.2 — DynamoDB Stream Processor (POLL Model)

This Lambda is invoked by the Lambda service which POLLS the DynamoDB Stream.
This is the POLL invocation model — Lambda service reads from the stream shards.

EXAM TIP: DynamoDB Streams use event source mappings (poll-based).
Lambda reads records in order within each shard.
Records are NOT removed from the stream after processing (unlike SQS).
Stream records expire after 24 hours regardless.
"""

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Process DynamoDB Stream records.
    
    EXAM TIP: The event contains a 'Records' array. Each record has:
      - eventName: INSERT, MODIFY, or REMOVE
      - dynamodb.Keys: The key attributes
      - dynamodb.NewImage: Item after the change (if stream view includes it)
      - dynamodb.OldImage: Item before the change (if stream view includes it)
      - dynamodb.StreamViewType: KEYS_ONLY, NEW_IMAGE, OLD_IMAGE, or NEW_AND_OLD_IMAGES
    """
    logger.info(f"Received {len(event['Records'])} DynamoDB Stream record(s)")
    
    for record in event['Records']:
        event_name = record['eventName']  # INSERT, MODIFY, REMOVE
        
        logger.info(f"--- {event_name} ---")
        
        # The key attributes are always present
        keys = record['dynamodb'].get('Keys', {})
        logger.info(f"Keys: {json.dumps(keys)}")
        
        if event_name == 'INSERT':
            # New item was created
            new_image = record['dynamodb'].get('NewImage', {})
            logger.info(f"New item created: {json.dumps(new_image)}")
            
            # EXAM TIP: Check for TTL deletions!
            # When DynamoDB TTL expires an item, it creates a REMOVE event
            # in the stream with userIdentity.type = "Service" and
            # userIdentity.principalId = "dynamodb.amazonaws.com".
            # This is FREE but appears in streams — useful for archiving!
            
        elif event_name == 'MODIFY':
            # Existing item was updated
            old_image = record['dynamodb'].get('OldImage', {})
            new_image = record['dynamodb'].get('NewImage', {})
            logger.info(f"Old values: {json.dumps(old_image)}")
            logger.info(f"New values: {json.dumps(new_image)}")
            
            # Compare old vs. new to detect specific changes
            # This is why NEW_AND_OLD_IMAGES is so useful
            
        elif event_name == 'REMOVE':
            # Item was deleted
            old_image = record['dynamodb'].get('OldImage', {})
            logger.info(f"Deleted item: {json.dumps(old_image)}")
            
            # Check if this was a TTL expiration
            identity = record.get('userIdentity', {})
            if identity.get('type') == 'Service':
                logger.info("This was a TTL expiration — could archive to S3!")
    
    # EXAM TIP: If this function raises an exception, the ENTIRE batch
    # will be retried. For DynamoDB Streams, this blocks the shard
    # until the batch succeeds or hits MaximumRetryAttempts.
    # Use BisectBatchOnFunctionError to split failed batches in half.
    
    return {'statusCode': 200, 'processed': len(event['Records'])}
