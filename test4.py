import boto3
from botocore.exceptions import ClientError

# Create an S3 client
s3 = boto3.client('s3')


https://iksaan.s3.ap-south-1.amazonaws.com/media/thumbnails/python_RAiptGb.webp
https://iksaan.s3.ap-south-1.amazonaws.com/media/thumbnails/python.webp



try:
    # Example operation: List objects in a specific bucket
    bucket_name = 'iksaan'
    response = s3.list_objects_v2(Bucket=bucket_name)
    print(response)
except ClientError as e:
    print(f"ClientError: {e}")

