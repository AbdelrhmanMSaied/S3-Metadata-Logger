import json 
import boto3 
import logging
import urllib.parse # Import to correctly decode S3 object keys


# Initialize S3 client
s3 = boto3.client('s3')

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # Parse the S3 event data for the recently uploaded image
    try:
        # NOTE: Using the number '0' and proper quotes
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        
        # S3 keys are URL-encoded, must be decoded
        object_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        # Log the recently uploaded image name
        logger.info(f"New image uploaded: {object_key} to bucket '{bucket_name}'")

        # Fetch and log all existing image names in the bucket
        existing_images = list_images_in_bucket(bucket_name)

        # NOTE: We are getting all metadata here, not just images.
        # This function fetches ALL objects and filters them for image extensions
        logger.info(f"All images in the bucket '{bucket_name}': {existing_images}")

        return {
            'statusCode': 200,
            'body': json.dumps(f"Logged recently uploaded image {object_key} and all existing images.")
        }
    
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        # Log the full event for deeper debugging
        logger.error(f"Full event data: {json.dumps(event)}")
        raise e


def list_images_in_bucket(bucket_name):
    """Fetch and return the list of all images in the given S3 bucket"""
    image_list = []

    # List objects in the bucket
    # Use the paginator for large buckets (best practice)
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name)
    
    for page in pages:
        # Check if page contains objects
        if 'Contents' in page:
            for obj in page['Contents']:
                # check if the object is an image (by extension)
                if obj['Key'].lower().endswith(('.jpg', '.jpeg', '.png')):
                    # Use 'Key' with a capital 'K' from the response
                    image_list.append(obj['Key'])

    return image_list