# Configuration Guide

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# AWS Configuration - Get these from your AWS account
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_HERE
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
AWS_DEFAULT_REGION=YOUR_AWS_REGION  # e.g., us-east-1, us-west-2, etc.

# SQS Queue URLs - Replace with your actual queue URLs after creating them
INPUT_QUEUE_URL=https://sqs.YOUR_AWS_REGION.amazonaws.com/YOUR_AWS_ACCOUNT_ID/YOUR_INPUT_QUEUE_NAME
OUTPUT_QUEUE_URL=https://sqs.YOUR_AWS_REGION.amazonaws.com/YOUR_AWS_ACCOUNT_ID/YOUR_OUTPUT_QUEUE_NAME

# S3 Bucket Names - Replace with your chosen bucket names (must be globally unique)
INPUT_BUCKET=YOUR_UNIQUE_INPUT_BUCKET_NAME
OUTPUT_BUCKET=YOUR_UNIQUE_OUTPUT_BUCKET_NAME

# EC2 Configuration for Auto Scaling - Get these from your AWS EC2 console
AMI_ID=YOUR_AMI_ID                    # e.g., ami-0abcdef1234567890
SECURITY_GROUP_ID=YOUR_SECURITY_GROUP_ID  # e.g., sg-0123456789abcdef0
SUBNET_ID=YOUR_SUBNET_ID              # e.g., subnet-0123456789abcdef0
```

## AWS Infrastructure Setup

### 1. S3 Buckets

Create two S3 buckets:

- **Input bucket**: For uploading images to be processed
- **Output bucket**: For storing processing results

```bash
# Replace 'your-unique-input-bucket-name' with your chosen bucket name
aws s3 mb s3://your-unique-input-bucket-name
# Replace 'your-unique-output-bucket-name' with your chosen bucket name
aws s3 mb s3://your-unique-output-bucket-name
```

### 2. SQS Queues

Create SQS queues for message processing:

```bash
# Input queue for processing requests - replace 'your-input-queue-name' with your chosen name
aws sqs create-queue --queue-name your-input-queue-name

# Output queue for results - replace 'your-output-queue-name' with your chosen name
aws sqs create-queue --queue-name your-output-queue-name
```

### 3. IAM Roles

#### EC2 Worker Role

Create an IAM role `EC2FaceWorkerRole` with the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": [
        "arn:aws:s3:::YOUR_INPUT_BUCKET_NAME/*",
        "arn:aws:s3:::YOUR_OUTPUT_BUCKET_NAME/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:SendMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": [
        "arn:aws:sqs:YOUR_AWS_REGION:YOUR_AWS_ACCOUNT_ID:YOUR_INPUT_QUEUE_NAME",
        "arn:aws:sqs:YOUR_AWS_REGION:YOUR_AWS_ACCOUNT_ID:YOUR_OUTPUT_QUEUE_NAME"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:RunInstances",
        "ec2:TerminateInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Lambda Execution Role

For the S3-to-SQS Lambda function:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:YOUR_AWS_REGION:YOUR_AWS_ACCOUNT_ID:YOUR_INPUT_QUEUE_NAME"
    }
  ]
}
```

## Application Configuration

### Spring Boot API (backend/api)

The Spring Boot application uses the following configuration in `application.properties`:

```properties
server.port=8080
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

### Python Services

All Python services read configuration from environment variables. Make sure to set:

- AWS credentials
- S3 bucket names
- SQS queue URLs
- EC2 configuration for auto-scaling

## Security Best Practices

1. **Use IAM Roles**: Prefer IAM roles over hardcoded credentials
2. **Enable S3 Encryption**: Enable server-side encryption on S3 buckets
3. **VPC Configuration**: Use private subnets for worker instances
4. **Security Groups**: Configure minimal required access
5. **CloudTrail**: Enable for audit logging
6. **Least Privilege**: Grant minimal required permissions

## Monitoring Setup

### CloudWatch Metrics

Monitor the following metrics:

- SQS queue length
- EC2 instance count
- S3 upload/download rates
- Lambda function errors

### Alarms

Set up CloudWatch alarms for:

- High queue length (scaling trigger)
- Failed processing attempts
- Unusual cost spikes
- Security events

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes the models directory
2. **Permission Denied**: Check IAM roles and policies
3. **Queue Empty**: Verify SQS queue URLs and Lambda triggers
4. **High Costs**: Review auto-scaling configuration and instance types

### Debugging Steps

1. Check CloudWatch logs for detailed error messages
2. Verify environment variables are set correctly
3. Test AWS credentials with `aws sts get-caller-identity`
4. Ensure data.pt file is in the correct location
5. Verify S3 bucket policies and permissions
