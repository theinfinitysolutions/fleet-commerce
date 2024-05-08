from django.contrib.auth.models import AbstractUser
from django.db import models

from fleet_commerce.mixin import AuthorTimeStampedModel


class BankDetails(AuthorTimeStampedModel):
    bank_account_holder_name = models.CharField(max_length=100, null=True)
    bank_account_number = models.CharField(max_length=18, null=True)
    ifsc_code = models.CharField(max_length=11, null=True)
    bank_name = models.CharField(max_length=100, null=True)
    branch_name = models.CharField(max_length=100, null=True)
    linked_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, null=True)


class DocumentDetails(AuthorTimeStampedModel):
    document = models.ForeignKey("utils.FileObject", null=True, on_delete=models.SET_NULL)
    linked_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100, null=True)


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    address = models.CharField(max_length=100, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True, null=True)
    pan_number = models.CharField(max_length=10, unique=True, null=True)
    verified = models.BooleanField(default=False)
    profile_image_url = models.URLField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_type = models.CharField(max_length=255, null=True, blank=True)
    salary_frequency = models.CharField(max_length=255, null=True, blank=True)
