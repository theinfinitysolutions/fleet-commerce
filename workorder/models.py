from django.db import models

from accounts.models import User
from billing.models import Invoice
from fleet.models import Machine
from utils.models import Customer
from fleet_commerce.mixin import AuthorTimeStampedModel


class WorkOrder(AuthorTimeStampedModel):
    work_order_number = models.CharField(max_length=100)
    agreement_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    machine = models.ManyToManyField(Machine, related_name="machines")
    site = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    special_instructions = models.CharField(max_length=500, null=True)
    resource_details = models.ManyToManyField(User, related_name="resources")
    billing_details = models.OneToOneField(Invoice, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, default="Confirmed")
