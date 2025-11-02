import os
import requests

# Update these variables with your actual values
upload_url = "http://localhost:8080/upload"  # Your Spring Boot API endpoint
bucket_name = "YOUR_INPUT_BUCKET_NAME"       # Replace with your S3 input bucket name
image_folder = "face_images_100"             # Path to your image folder

for image_name in os.listdir(image_folder):
    if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(image_folder, image_name)
    key = f"input/{image_name}"
    print(key)

    with open(image_path, "rb") as f:
        files = {"file": (image_name, f)}
        data = {
            "bucket": bucket_name,
            "key": key
        }
        print(f"Uploading {image_name} to {key}...")

        response = requests.post(upload_url, files=files, data=data)

        if response.status_code == 202:
            print(f"Uploaded: {image_name}")
        else:
            print(f"Failed to upload {image_name}: {response.text}")
