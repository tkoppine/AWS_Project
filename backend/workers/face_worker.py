import os
import json 
import boto3
import tempfile
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.face_recognition import face_match


INPUT_QUEUE_URL = os.getenv("INPUT_QUEUE_URL")
OUTPUT_QUEUE_URL = os.getenv("OUTPUT_QUEUE_URL")
INPUT_BUCKET = os.getenv("INPUT_BUCKET")
OUTPUT_BUCKET = os.getenv("OUTPUT_BUCKET")

print("DEBUG  INPUT_BUCKET:", INPUT_BUCKET, "OUTPUT_BUCKET:", OUTPUT_BUCKET)

s3 = boto3.client("s3", region_name="us-east-2")
sqs = boto3.client("sqs", region_name="us-east-2")


def process_message(message):
    body = json.loads(message['Body'])
    print("DEBUG Message Body:", message['Body'])
    s3_key = body['key']

    print(f"Received Message for {s3_key}")

    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        s3.download_file(INPUT_BUCKET, s3_key, tmp.name)

        try:
            data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'data.pt')
            name, distance = face_match(tmp.name, data_path)
        except Exception as e:
            print(f"Error processing {s3_key}: {e}")
            name, distance = "error", -1
        

        result = {
            "input_image": s3_key,
            "matched_name": name,
            "distance": distance
        }

        output_key = s3_key.replace("input/", "output/") + ".json"
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=output_key, Body=json.dumps(result))


        sqs.send_message(
            QueueUrl = OUTPUT_QUEUE_URL,
            MessageBody = json.dumps({
                "bucket" : OUTPUT_BUCKET,
                "key" : output_key,
                "matched_name" : name,
                "distance" : distance
            })
        )


        sqs.delete_message(
            QueueUrl = INPUT_QUEUE_URL,
            ReceiptHandle = message["ReceiptHandle"]
        )

        print(f"Processed {s3_key} -> Matched: {name} (Distance: {distance})")


def main():
    print("Face Worker Running....")

    while True:
        response = sqs.receive_message(
            QueueUrl = INPUT_QUEUE_URL,
            MaxNumberOfMessages = 1,
            WaitTimeSeconds = 20
        )

        messages = response.get("Messages", [])
        if messages:
            for message in messages:
                process_message(message)
        else:
            print("Waiting for messages...")


if __name__ == "__main__":
    main()