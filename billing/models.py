from django.db import models

from product.models import TimeStampedModel

# Create your models here.

class Invoice(TimeStampedModel):
    UNPAID = "unpaid"
    UNDERPAID = "underpaid"
    OVERPAID = "overpaid"
    FULLY_PAID = "fully_paid"
    COMBINED_FULLY_PAID = "combined_fully_paid"

    PAYMENT_STATUS_CHOICES = (
        (UNPAID, UNPAID),
        (UNDERPAID, UNDERPAID),
        (OVERPAID, OVERPAID),
        (FULLY_PAID, FULLY_PAID),
    )

    invoice_date = models.DateField()
    invoice_number = models.CharField(max_length=64)
    due_date = models.DateField(null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withholding_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_payable = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=24, default=UNPAID, choices=PAYMENT_STATUS_CHOICES)

    payer = models.CharField(max_length=24, null=True, blank=True)
    payee = models.CharField(max_length=24, null=True, blank=True)
