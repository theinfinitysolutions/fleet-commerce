import os

import boto3


class S3Utils:
    def initialize_boto3():
        region_name = os.getenv("AWS_REGION_NAME", "ap-southeast-1")
        return boto3.client(
            "s3", region_name=region_name, endpoint_url=f"https://s3.{region_name}.amazonaws.com"
        )

    @staticmethod
    def generate_s3_url(bucket_name, object_key, expiry=3600):
        s3_client = S3Utils.initialize_boto3()
        return s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket_name, "Key": object_key}, ExpiresIn=expiry
        )  # URL expires in 1 hour
