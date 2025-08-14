package com.aws.lambda;

import static java.lang.System.getenv;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.events.S3Event;

import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;

public class S3ToSqsHandler 
{
    private static final String QUEUE_URL = getenv("SQS_QUEUE_URL");

    public void handleRequest(S3Event event, Context context){
        SqsClient sqs = SqsClient.create();


        event.getRecords().forEach(record -> {
            String bucket = record.getS3().getBucket().getName();

            String key = record.getS3().getObject().getKey();

            context.getLogger().log("Bucket: " + bucket + ", Key: " + key + "\n");
            
            String message = String.format("{\"bucket\": \"%s\", \"key\": \"%s\"}", bucket, key);

            SendMessageRequest req = SendMessageRequest.builder()
                    .queueUrl(QUEUE_URL)
                    .messageBody(message)
                    .build();
            sqs.sendMessage(req);

            context.getLogger().log("Sent message to SQS.\n");
        });

        sqs.close();
    }
}
