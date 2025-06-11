import boto3
import urllib.parse
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')

# Set the destination bucket and SNS topic ARN
DEST_BUCKET = 'backup-bucket-shreya'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:538827147631:file-backup-alerts'

def lambda_handler(event, context):
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        file_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        if source_bucket == DEST_BUCKET:
            print(f"Skipping backup for file {file_key} from backup bucket itself.")
            continue

        copy_source = {'Bucket': source_bucket, 'Key': file_key}
        s3.copy_object(CopySource=copy_source, Bucket=DEST_BUCKET, Key=file_key)

        message = f"File '{file_key}' has been backed up from '{source_bucket}' to '{DEST_BUCKET}'."
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Auto Backup Alert"
        )

    return {
        'statusCode': 200,
        'body': 'Backup and notification completed successfully.'
    }
