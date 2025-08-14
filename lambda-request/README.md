# AWS S3 → Lambda → SQS → EC2 Face Processing Pipeline

This project implements a Java AWS Lambda handler that listens to **S3 image uploads** and sends messages to **Amazon SQS**.  
An EC2 worker (or a pool of workers) reads from the queue and processes the images (e.g., face recognition).

The design is **event-driven**, **scalable**, and **decoupled**.

---

## 1. How the System Works (Complete Flow)

1. **Image Upload to S3**
   - A new image is uploaded to the input S3 bucket (e.g., `input/photo.jpg`).
2. **S3 Event Trigger**

   - S3 triggers the **Lambda function** by sending an event containing the bucket name and object key.

3. **Lambda Handler (S3ToSqsHandler.java)**
   - Reads the SQS queue URL from the environment variable `SQS_QUEUE_URL`.
   - For each uploaded file in the event:
     - Extracts **bucket** and **key**.
     - Logs them to CloudWatch.
     - Creates a JSON message:
       ```json
       { "bucket": "<bucket>", "key": "<key>" }
       ```
     - Sends the message to the configured SQS queue.
4. **SQS Queue**

   - Holds messages until they are processed.
   - Decouples the upload event from the processing logic.

5. **EC2 Worker**
   - Continuously polls the SQS queue for new messages.
   - When a message is received, it:
     - Downloads the image from S3.
     - Processes it (e.g., runs face recognition).
     - Stores the results in an output S3 bucket.
     - Optionally sends a completion message to another queue.åß
