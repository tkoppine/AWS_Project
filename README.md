# AWS Face Recognition Worker System

This project is a **scalable face recognition system** running on AWS.  
It uses **EC2**, **S3**, **SQS**, and **Boto3** to automatically scale worker instances based on the size of an input queue, process images for face matching, and send results back to an output queue.

---

## 1. Overview

The system works in four main steps:

1. **Scaling Controller** — Monitors an SQS input queue and launches/terminates EC2 worker instances based on workload.
2. **Worker (Face Processor)** — Downloads images from S3, runs face recognition, and uploads the results back to S3 and SQS.
3. **Face Recognition Model** — Uses `facenet-pytorch` to match faces against stored embeddings.
4. **Image Uploader** — Sends images to the input S3 bucket and notifies the system.

---

## 2. Components

### A. Auto Scaling Controller

- Monitors:
  - **Number of messages** in the SQS input queue.
  - **Number of running EC2 worker instances**.
- **Scaling logic**:
  - If the queue is empty → terminate all workers.
  - If there are more messages than running instances → launch more workers (up to a limit).
  - If there are fewer messages than running instances → scale down workers.
- Workers are EC2 instances with the role **FaceWorker** that start processing automatically on boot.

**Key AWS Services Used:**

- **SQS** — Input queue for images.
- **EC2** — Worker instances.
- **IAM Role** — Grants workers access to S3 and SQS.

---

### B. Face Worker (`face_worker.py`)

- Waits for new messages from the SQS input queue.
- For each message:
  1. Downloads the image from the input S3 bucket.
  2. Runs `face_match()` to identify the person.
  3. Saves results as a `.json` file in the output S3 bucket.
  4. Sends a message to the output SQS queue with match details.
  5. Deletes the original message from the input queue.

---

### C. Face Matching (`face_recognition.py`)

- Loads a pre-trained **InceptionResnetV1** model from `facenet-pytorch`.
- Detects a face using **MTCNN**.
- Generates a face embedding and compares it with stored embeddings (`data.pt`).
- Returns the **closest matching name** and the **distance score**.

---

### D. Image Uploader (`uploader.py`)

- Reads images from a local folder.
- Uploads them to the input S3 bucket with a key prefix `input/`.
- Sends metadata to a local API endpoint (`/upload`) to trigger processing.

---

## 3. Environment Variables

These must be set before running the scripts:

| Variable            | Description                   |
| ------------------- | ----------------------------- |
| `INPUT_QUEUE_URL`   | URL of the SQS input queue.   |
| `OUTPUT_QUEUE_URL`  | URL of the SQS output queue.  |
| `INPUT_BUCKET`      | Name of the S3 input bucket.  |
| `OUTPUT_BUCKET`     | Name of the S3 output bucket. |
| `AMI_ID`            | AMI ID for worker instances.  |
| `SECURITY_GROUP_ID` | Security group for workers.   |
| `SUBNET_ID`         | Subnet ID for workers.        |

---

## 4. How It Works — Step by Step

1. **Upload Images**

   - Run the uploader script to send images to S3 and add a message to the SQS input queue.

2. **Controller Starts Workers**

   - The controller script monitors the input queue length.
   - Launches new EC2 FaceWorker instances when needed.

3. **Workers Process Images**

   - Each worker downloads the assigned image from S3.
   - Runs face recognition using stored embeddings.
   - Uploads the JSON result to the output S3 bucket.
   - Sends a result message to the output SQS queue.

4. **Controller Scales Down**
   - When the queue is empty, all workers are terminated automatically.

---

## 5. Requirements

Install dependencies:

```bash
pip install boto3 facenet-pytorch pillow torch requests
```
