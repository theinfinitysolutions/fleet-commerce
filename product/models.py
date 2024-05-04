from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampedModel


class Product(TimeStampedModel):
    vehicle_number = models.CharField(max_length=56)
    make_name = models.CharField(max_length=56)
    model_name = models.CharField(max_length=56)
    model_year = models.IntegerField(null=True, blank=True)
    cc = models.IntegerField(null=True, blank=True)
    sub_model_name = models.CharField(max_length=56, blank=True, null=True)
    chassis_number = models.CharField(max_length=56, blank=True, null=True)
    engine_number = models.CharField(max_length=56, blank=True, null=True)
    odometer_reading = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=56, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict)
    purchased_date = models.DateField(null=True, blank=True)
    product_image = models.URLField(blank=True, null=True)


class Contract(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="contracts"
    )
    supervisor = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="supervised_contracts"
    )
    main_driver = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="main_driver_contracts"
    )
    support_staffs = models.ManyToManyField("accounts.User", related_name="support_staff_contracts")
    vendor = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="vendor_contracts"
    )
    contract_start_date = models.DateField(null=True, blank=True)
    contract_expiry_date = models.DateField(null=True, blank=True)
    initial_odometer_reading = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    invoice = models.ForeignKey(
        "billing.Invoice", on_delete=models.SET_NULL, null=True, related_name="contracts"
    )
    is_active = models.BooleanField(default=True)
    start_odometer_reading = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    final_odometer_reading = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )


class ReadingTransaction(TimeStampedModel):
    FUEL = "fuel"
    ODOMETER = "odometer"
    READING_TYPE_CHOICES = (
        (FUEL, FUEL),
        (ODOMETER, ODOMETER),
    )
    reading = models.IntegerField(null=True, blank=True)
    reading_type = models.CharField(max_length=24, null=True, choices=READING_TYPE_CHOICES)
    contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, null=True, related_name="reading_transactions"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="reading_transactions"
    )
    metadata = models.JSONField(default=dict)


class DailyAttendance(TimeStampedModel):
    employee = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="daily_attendances"
    )
    shift_start_time = models.DateTimeField()
    shift_end_time = models.DateTimeField(blank=True, null=True)
    contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, null=True, related_name="daily_attendances"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="attended_products"
    )


class Reimbursement(TimeStampedModel):
    employee = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="reimbursements"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="reimbursements"
    )
    contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, null=True, related_name="reimbursements"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()


class IssueReport(TimeStampedModel):
    STATUS_CHOICES = (
        ("reported", "Reported"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )
    reporter = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="reported_issues"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="product_issues"
    )
    contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, null=True, related_name="contract_issues"
    )
    description = models.TextField()
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default="reported")
