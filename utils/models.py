import os

from django.db import models

from fleet_commerce.mixin import AuthorTimeStampedModel, OrganisationTimeStampedModel


# Create your models here.
class FileObject(AuthorTimeStampedModel):
    original_file_name = models.CharField(max_length=100, blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    s3_key = models.CharField(max_length=100, blank=True, null=True)
    s3_bucket = models.CharField(max_length=100, blank=True, null=True)
    size = models.IntegerField(max_length=100, blank=True, null=True)

    @property
    def s3_url(self):
        from utils.utils import S3Utils

        return S3Utils.generate_s3_url(self.s3_bucket, self.s3_key)

    @property
    def cloudfront_url(self):
        cloudfront_url = os.getenv("CLOUDFRONT_URL")
        if cloudfront_url is None:
            return self.s3_url

        return f"{cloudfront_url}/{self.s3_key}"


class Location(OrganisationTimeStampedModel):
    location = models.CharField(max_length=100, blank=True, null=True)
    custodian_name = models.CharField(max_length=100, blank=True, null=True)
    address_line1 = models.CharField(max_length=100, blank=True, null=True)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=100, blank=True, null=True)


class Customer(OrganisationTimeStampedModel):
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
