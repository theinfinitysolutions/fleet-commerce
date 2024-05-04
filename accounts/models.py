from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator

from product.models import TimeStampedModel


class BaseUser(AbstractUser):
    settings = models.JSONField(default=dict)

class BankDetails(TimeStampedModel):
    aadhar_validator = RegexValidator(regex=r'^\d{12}$',message="Aadhar number must consist of 12 digits")
    pan_validator = RegexValidator(regex=r'^[A-Z]{5}\d{4}[A-Z]{1}$', message="PAN must be in the format: ABCDE1234F")
    account_number_validator = MinLengthValidator(limit_value=9,message="Account number must be at least 9 digits long")
    ifsc_validator = RegexValidator(regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',message="IFSC must be in the format: ABCD0EFGHIJ")

    aadhar_number = models.CharField(max_length=12,unique=True,validators=[aadhar_validator],help_text="Enter 12-digit Aadhar number")
    pan_number = models.CharField(max_length=10,unique=True,validators=[pan_validator],help_text="Enter valid PAN number")
    bank_account_number = models.CharField(max_length=18,validators=[account_number_validator],help_text="Enter your bank account number")
    ifsc_code = models.CharField(max_length=11,validators=[ifsc_validator],help_text="Enter IFSC code of the bank branch")
    bank_branch = models.CharField(max_length=100,help_text="Enter the name of the bank branch")

class DocumentDetails(TimeStampedModel):
    aadhar_card = models.ForeignKey("utils.FileObject", null=True, on_delete=models.SET_NULL)

class User(BaseUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    name = models.CharField()
    phone = models.CharField(validators=[phone_regex], max_length='17', blank=True)
    email = models.EmailField(max_length='100',unique=True)
    address = models.CharField(max_length='100')
    bank_details = models.OneToOneField(BankDetails,on_delete=models.CASCADE)
    document_details = models.OneToOneField(DocumentDetails,on_delete=models.CASCADE)
