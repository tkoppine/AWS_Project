# ScaleVision: AI-Powered Face Recognition on AWS

A scalable, event-driven face recognition system built on AWS infrastructure that automatically processes images using EC2 workers, S3 storage, and SQS queues.

## 🏗️ Project Structure

```
/
├── backend/                     # Backend services and processing
│   ├── api/                    # Spring Boot REST API for file uploads
│   ├── models/                 # Face recognition models and utilities
│   │   ├── face_recognition.py # Core face matching logic
│   │   └── names.py           # Utility to display available names
│   ├── services/               # Auto-scaling and management services
│   │   └── auto_scale.py      # EC2 auto-scaling controller
│   └── workers/                # Background processing workers
│       └── face_worker.py     # Main face processing worker
├── aws/                        # AWS infrastructure components
│   └── lambda/                 # Lambda functions
│       ├── pom.xml            # Maven configuration for Lambda
│       └── src/               # Lambda source code
├── data/                       # Training data and images
│   ├── data.pt                # Pre-trained face embeddings
│   └── face_images_100/       # Sample face images
├── docs/                       # Documentation
│   └── original_README.md     # Original project documentation
└── scripts/                    # Utility and deployment scripts
    ├── Send_Images.py         # Image upload utility
    └── start_script.sh        # Worker startup script
```

## 🚀 Features

- **Auto-scaling**: Automatically launches and terminates EC2 instances based on queue length
- **Face Recognition**: Uses FaceNet for accurate face matching with pre-trained embeddings
- **Event-driven**: S3 uploads trigger Lambda functions that queue processing tasks
- **Scalable Architecture**: Decoupled components using SQS for reliable message processing
- **REST API**: Spring Boot application for easy file uploads and integration

## 🛠️ Technology Stack

### Backend

- **Python 3.8+** - Core processing logic
- **PyTorch** - Deep learning framework
- **FaceNet-PyTorch** - Pre-trained face recognition models
- **Java 17** - Spring Boot API
- **Spring Boot 3.x** - REST API framework

### AWS Services

- **EC2** - Auto-scaling worker instances
- **S3** - Image storage (input/output buckets)
- **SQS** - Message queues for task coordination
- **Lambda** - Event-driven processing triggers
- **IAM** - Security and access management

## 📋 Prerequisites

### System Requirements

- Python 3.8 or higher
- Java 17 or higher
- AWS CLI configured with appropriate credentials
- Maven for Java builds

### Python Dependencies

```bash
pip install torch torchvision facenet-pytorch pillow boto3 requests
```

### AWS Resources Required

- Input S3 bucket for image uploads
- Output S3 bucket for processing results
- Input SQS queue for processing requests
- Output SQS queue for results
- IAM roles for EC2 workers and Lambda functions
- Security groups and VPC configuration

## 🔧 Environment Configuration

Set the following environment variables:

```bash
# AWS Configuration - Replace with your actual AWS credentials
export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_HERE
export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
export AWS_DEFAULT_REGION=YOUR_AWS_REGION  # e.g., us-east-1, us-west-2, etc.

# SQS Queue URLs - Replace with your actual queue URLs
export INPUT_QUEUE_URL=https://sqs.YOUR_AWS_REGION.amazonaws.com/YOUR_AWS_ACCOUNT_ID/YOUR_INPUT_QUEUE_NAME
export OUTPUT_QUEUE_URL=https://sqs.YOUR_AWS_REGION.amazonaws.com/YOUR_AWS_ACCOUNT_ID/YOUR_OUTPUT_QUEUE_NAME

# S3 Bucket Names - Replace with your unique bucket names
export INPUT_BUCKET=YOUR_UNIQUE_INPUT_BUCKET_NAME
export OUTPUT_BUCKET=YOUR_UNIQUE_OUTPUT_BUCKET_NAME

# EC2 Configuration (for auto-scaling) - Replace with your AWS resource IDs
export AMI_ID=YOUR_AMI_ID                    # e.g., ami-0abcdef1234567890
export SECURITY_GROUP_ID=YOUR_SECURITY_GROUP_ID  # e.g., sg-0123456789abcdef0
export SUBNET_ID=YOUR_SUBNET_ID              # e.g., subnet-0123456789abcdef0
```

## 🚦 Quick Start

### 1. Start the Spring Boot API

```bash
cd backend/api
./mvnw spring-boot:run
```

The API will be available at `http://localhost:8080`

### 2. Start the Auto-Scaler

```bash
cd backend/services
python auto_scale.py
```

### 3. Upload Images for Processing

```bash
cd scripts
python Send_Images.py
```

### 4. Monitor Workers

The auto-scaler will automatically launch EC2 instances as needed to process the queue.

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Image Upload  │───▶│   S3 Bucket     │───▶│  Lambda Trigger │
│   (REST API)    │    │   (Input)       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Auto Scaler    │◀───│  SQS Queue      │◀───│  Message Queue  │
│  (EC2 Manager)  │    │  (Input)        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  EC2 Workers    │───▶│  Face Recognition│───▶│  S3 Bucket      │
│  (Face Proc.)   │    │  Processing     │    │  (Output)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔒 Security Considerations

- Use IAM roles instead of hardcoded credentials
- Enable S3 bucket encryption
- Configure VPC security groups properly
- Use private subnets for worker instances
- Enable CloudTrail for audit logging

## 📈 Monitoring and Scaling

- **CloudWatch Metrics**: Monitor queue length, instance count, and processing times
- **Auto Scaling**: Configurable min/max instance limits
- **Error Handling**: Comprehensive error logging and dead letter queues
- **Cost Optimization**: Automatic termination of idle instances
