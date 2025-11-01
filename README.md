# S3-Metadata-Logger
This project implements a foundational serverless, event-driven architecture (EDA) on AWS. The primary function is to automatically capture and log critical metadata for every file uploaded, deleted or modified to a designated S3 bucket in real-time

 # Architecture and Workflow
 The solution establishes a reliable, near real-time data pipeline consisting of three main services:

1. Event Source (Amazon S3): A designated S3 bucket is configured to monitor for object events 

2. Compute Layer (AWS Lambda): The Python-based MetadataLogger function is triggered asynchronously by the S3 event.

3. Observability (AWS CloudWatch): The Lambda function automatically publishes execution details and custom application logs to a dedicated CloudWatch Log Group.

Workflow: When a file is uploaded to the S3 bucket, the event notification invokes the Lambda function. The function then uses the AWS SDK (boto3), retrieving the full file metadata (size, content type, ETag, etc.) without downloading the file body, and logging these details to CloudWatch.

Note: The function's IAM role uses AmazonS3FullAccess for simplified setup, but its execution is constrained. The code is only invoked when triggered by a configured S3 bucket, meaning this broad permission does not result in the code acting on every bucket in the account.
