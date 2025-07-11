import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

s3 = boto3.client('s3')

try:
    response = s3.list_buckets()
    print(response)
except (NoCredentialsError, PartialCredentialsError):
    print("Credentials are not configured correctly.")
except ClientError as e:
    print(f"ClientError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
