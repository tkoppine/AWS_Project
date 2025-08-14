#!/bin/bash
export INPUT_QUEUE_URL=https://sqs.us-east-2.amazonaws.com/012560051368/face-recognition-request-queue
export OUTPUT_QUEUE_URL=https://sqs.us-east-2.amazonaws.com/012560051368/face-recognition-response-queue
export INPUT_BUCKET=asuinputbucket
export OUTPUT_BUCKET=asuoutputbucket

cd /home/ec2-user
python3 face_worker.py