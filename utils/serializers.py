import os
import re
import time

import magic
from django.core.files.storage import default_storage
from rest_framework import serializers

from utils.utils import S3Utils

from .models import FileObject


class FileObjectSerializer(serializers.ModelSerializer):
    s3_url = serializers.SerializerMethodField()

    class Meta:
        model = FileObject
        fields = "__all__"

    def get_s3_url(self, obj):
        return obj.s3_url


class CreateFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = FileObject
        fields = "file"

    def create(self, validated_data):
        file = validated_data["file"]

        aws_s3_bucket = os.getenv("AWS_S3_BUCKET_NAME")
        # Remove unwanted characters from file name
        safe_file_name = re.sub("[^a-zA-Z0-9_.]", "_", file.name)

        ts = int(time.time())
        key = f"fleet-image/{ts}_{safe_file_name}"

        s3_client = S3Utils.initialize_boto3()
        file.seek(0)  # Reset the file pointer to the beginning
        s3_client.upload_fileobj(file, aws_s3_bucket, key)

        file.seek(0)
        file_mime = magic.from_buffer(file.read(), mime=True)
        file_obj = FileObject.objects.create(
            original_file_name=file.name,
            mime_type=file_mime,
            size=file.size,
            s3_key=key,
            s3_bucket=aws_s3_bucket,
        )

        return file_obj