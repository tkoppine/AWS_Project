#!/bin/bash
# Replace YOUR_AWS_ACCOUNT_ID with your actual AWS account ID
export INPUT_QUEUE_URL=https://sqs.YOUR_AWS_REGION.amazonaws.com/YOUR_AWS_ACCOUNT_ID/YOUR_INPUT_QUEUE_NAME
export OUTPUT_QUEUE_URL=https://sqs.YOUR_AWS_REGION.amazonaws.com/YOUR_AWS_ACCOUNT_ID/YOUR_OUTPUT_QUEUE_NAME
# Replace with your actual S3 bucket names
export INPUT_BUCKET=YOUR_INPUT_BUCKET_NAME
export OUTPUT_BUCKET=YOUR_OUTPUT_BUCKET_NAME

cd /home/ec2-user
python3 face_worker.py