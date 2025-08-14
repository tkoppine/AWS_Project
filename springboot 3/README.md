# AWS S3 File Upload – Spring Boot Project

## 📌 Overview

This project demonstrates how to upload files to an **AWS S3 bucket** using **Spring Boot** and the **AWS SDK v2**.  
It provides a REST API endpoint where users can send a file, specify the bucket and key, and store the file in S3.

## 🚀 Features

- Upload any file to an AWS S3 bucket.
- Accepts bucket name, file key, and file through a REST API.
- Configurable AWS credentials and region.
- Supports large file uploads (up to 50MB in this setup).

## 📂 Project Structure

src/main/java/com/aws/springboot/
│
├── config/
│ └── StorageConfig.java # AWS S3 client configuration
│
├── controller/
│ └── S3Controller.java # REST endpoint for file upload
│
├── service/
│ └── S3Service.java # Upload logic using AWS SDK

## ⚙️ Technologies Used

- **Java 17+**
- **Spring Boot**
- **AWS SDK for Java v2**
- **Lombok**
- **Maven**

## 🔑 AWS Setup

1. Create an **AWS account**.
2. Create an **S3 bucket**.
3. Create an **IAM user** with `AmazonS3FullAccess` permissions.
4. Obtain **AWS Access Key** and **Secret Key**.

## ⚙️ Configuration

### Environment Variables (Recommended)

```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key


Architecture Flow
[Client Request]
      |
      v
[Spring Boot Controller] --> Receives request parameters & file
      |
      v
[Service Layer] --> Calls AWS S3 SDK with credentials & file data
      |
      v
[AWS S3] --> Stores the file in the specified bucket
      |
      v
[Response Sent Back to Client with ETag]
```
