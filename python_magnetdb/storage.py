from os import getenv

from minio import Minio

s3_client = Minio(
    getenv('S3_ENDPOINT'),
    access_key=getenv("S3_ACCESS_KEY"),
    secret_key=getenv("S3_SECRET_KEY"),
    secure=False
)
s3_bucket = getenv("S3_BUCKET")

if not s3_client.bucket_exists(s3_bucket):
    s3_client.make_bucket(s3_bucket)
