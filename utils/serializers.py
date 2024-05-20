import os
import re
import time
from io import BytesIO

import magic
from django.core.files.storage import default_storage
from rest_framework import serializers

from utils.utils import S3Utils

from .models import FileObject, Location


class FileObjectSerializer(serializers.ModelSerializer):
    s3_url = serializers.SerializerMethodField()
    cloudfront_url = serializers.SerializerMethodField()

    class Meta:
        model = FileObject
        fields = "__all__"

    def get_s3_url(self, obj):
        return obj.s3_url
    
    def get_cloudfront_url(self, obj):
        return obj.cloudfront_url


class CreateFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = FileObject
        fields = "__all__"

    def create(self, validated_data):
        file = validated_data["file"]

        aws_s3_bucket = os.getenv("AWS_S3_BUCKET_NAME")
        # Remove unwanted characters from file name
        safe_file_name = re.sub("[^a-zA-Z0-9_.]", "_", file.name)

        ts = int(time.time())
        key = f"fleet-image/{ts}_{safe_file_name}"

        s3_client = S3Utils.initialize_boto3()
        # Read the file content into memory
        file_content = file.read()

        # Reset the stream for further processing
        file_stream = BytesIO(file_content)
        file_stream.seek(0)
        file_mime = magic.from_buffer(file_stream.read(), mime=True)

        # Upload the file object to S3 using the content in memory
        file_stream = BytesIO(file_content)
        s3_client.upload_fileobj(file_stream, aws_s3_bucket, key)
       
        file_obj = FileObject.objects.create(
            original_file_name=file.name,
            mime_type=file_mime,
            size=file.size,
            s3_key=key,
            s3_bucket=aws_s3_bucket,
        )

        return file_obj


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
