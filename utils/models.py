from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# Create your models here.
class FileObject(TimeStampedModel):
    original_file_name = models.CharField(max_length=100)
    mime_type = models.CharField(max_length=100)
    s3_key = models.CharField(max_length=100)
    s3_bucket = models.CharField(max_length=100)
    size = models.IntegerField(max_length=100)

    @property
    def s3_url(self):
        from utils.utils import S3Utils

        return S3Utils.generate_s3_url(self.s3_bucket, self.s3_key)
