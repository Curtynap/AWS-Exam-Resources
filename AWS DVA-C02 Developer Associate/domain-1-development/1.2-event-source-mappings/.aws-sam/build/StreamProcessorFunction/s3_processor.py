"""
DVA-C02 Task 1.2 — S3 Event Processor (PUSH Model)

This Lambda is invoked DIRECTLY by S3 when an object is created.
S3 sends the event synchronously — this is the PUSH invocation model.

EXAM TIP: S3 event notifications are push-based.
S3 invokes Lambda directly. There is NO event source mapping.
The notification is configured on the S3 bucket, not on Lambda.
"""

import json
import logging
import urllib.parse

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    """
    Process S3 object creation events.
    
    EXAM TIP: The S3 event structure contains a 'Records' array.
    Each record has:
      - s3.bucket.name — the bucket
      - s3.object.key — the object key (URL-encoded!)
      - s3.object.size — file size in bytes
      - eventName — e.g., "ObjectCreated:Put"
    """
    logger.info(f"Received S3 event with {len(event['Records'])} record(s)")
    
    for record in event['Records']:
        # Extract event details
        event_name = record['eventName']
        bucket = record['s3']['bucket']['name']
        
        # EXAM TIP: S3 object keys are URL-encoded in the event.
        # A file named "my file.txt" arrives as "my+file.txt".
        # You MUST decode it before using it with the S3 SDK.
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        size = record['s3']['object'].get('size', 0)
        
        logger.info(f"Event: {event_name}")
        logger.info(f"Bucket: {bucket}")
        logger.info(f"Key: {key}")
        logger.info(f"Size: {size} bytes")
        
        # In a real app, you might:
        # - Generate thumbnails for images
        # - Transcode audio/video files
        # - Extract text from PDFs
        # - Index the content in a search engine
        
        # Example: Read the object metadata
        try:
            response = s3_client.head_object(Bucket=bucket, Key=key)
            content_type = response.get('ContentType', 'unknown')
            logger.info(f"Content-Type: {content_type}")
            
            # EXAM TIP: For media processing (images, audio, video):
            # - Small files (<6MB): Process directly in Lambda
            # - Large files (>6MB): Lambda can still process up to 10GB via /tmp
            # - Very large files: Trigger Step Functions or MediaConvert instead
            
        except Exception as e:
            logger.error(f"Error reading object metadata: {str(e)}")
            raise
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Processed {len(event["Records"])} S3 event(s)'})
    }
