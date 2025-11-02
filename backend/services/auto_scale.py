import boto3
import time
import os

INPUT_QUEUE_URL = os.getenv("INPUT_QUEUE_URL")
OUTPUT_QUEUE_URL = os.getenv("OUTPUT_QUEUE_URL")
INPUT_BUCKET = os.getenv("INPUT_BUCKET")
OUTPUT_BUCKET = os.getenv("OUTPUT_BUCKET")


#CONFIG
AMI_ID = os.getenv("AMI_ID")
INSTANCE_TYPE = 't2.micro'
MAX_INSTANCES = 2
INSTANCE_TAG_KEY = 'Role'
INSTANCE_TAG_VALUE = 'FaceWorker'
IAM_INSTANCE_PROFILE = 'EC2FaceWorkerRole'
SECURITY_GROUP_ID = os.getenv("SECURITY_GROUP_ID")
SUBNET_ID = os.getenv("SUBNET_ID")
REGION = 'us-east-2'


ec2 = boto3.client('ec2', region_name='us-east-2')
sqs = boto3.client('sqs', region_name='us-east-2')

def get_queue_length():
    attributes = sqs.get_queue_attributes(
        QueueUrl=INPUT_QUEUE_URL,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(attributes['Attributes']['ApproximateNumberOfMessages'])

def get_running_instances():
    response = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{INSTANCE_TAG_KEY}', 'Values': [INSTANCE_TAG_VALUE]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    instances = [i['InstanceId'] for r in response['Reservations'] for i in r['Instances']]
    
    return instances

def launch_instances(count):
    print(f"Launching {count} instance(s)...")

    user_data_script = """#!/bin/bash
cd /home/ec2-user
source ~/.bashrc
nohup python3 face_worker.py > face_worker.log 2>&1 &
"""
    # Define the environment config to inject
    ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        MinCount=count,
        MaxCount=count,
        SubnetId=SUBNET_ID,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        IamInstanceProfile={'Name': IAM_INSTANCE_PROFILE},
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': INSTANCE_TAG_KEY, 'Value': INSTANCE_TAG_VALUE}]
        }],
        UserData=user_data_script
    )


def terminate_all_faceworkers():
    instances = get_running_instances()

    if instances:
        print(f"Terminating instances: {instances}")
        ec2.terminate_instances(InstanceIds=instances)
    else:
        print("No running instances to terminate.")


def main():
    MIN_INSTANCES = 1

    while True:
        queue_length = get_queue_length()
        running_instances = get_running_instances()
        no_of_instances = len(running_instances)

        print(f"Queue length: {queue_length}, Running instances: {no_of_instances}")

        if queue_length == 0 and no_of_instances > 0:
            print("Queue empty. Terminating all workers.")
            terminate_all_faceworkers()

        elif queue_length > no_of_instances:
            to_launch = min(queue_length - no_of_instances, MAX_INSTANCES - no_of_instances)
            if to_launch > 0:
                launch_instances(to_launch)

        elif queue_length < no_of_instances and no_of_instances > MIN_INSTANCES:
            to_terminate = min(no_of_instances - queue_length, 1)
            instances_to_terminate = running_instances[:to_terminate]
            print(f"Scaling down. Terminating: {instances_to_terminate}")
            ec2.terminate_instances(InstanceIds=instances_to_terminate)

        time.sleep(30)

if __name__ == "__main__":
    main()