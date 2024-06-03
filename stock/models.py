from django.db import models

from fleet_commerce.mixin import OrganisationTimeStampedModel
from fleet.models import Machine
from workorder.models import WorkOrder

class SparePart(OrganisationTimeStampedModel):
    FUEL = "fuel"
    MECHANICAL_PART = "mechanical_part"
    ELECTRICAL_PART = "electrical_part"
    LUBRICANT = "lubricant"
    OTHER = "other"

    CATEGORY_CHOICES = (
        (FUEL, FUEL),
        (MECHANICAL_PART, MECHANICAL_PART),
        (ELECTRICAL_PART, ELECTRICAL_PART),
        (LUBRICANT, LUBRICANT),
        (OTHER, OTHER),
    )

    BRAND_NEW = "brand_new"
    USED = "used"
    EXHAUSTED = "exhausted"

    STATUS_CHOICES = (
        (BRAND_NEW, BRAND_NEW),
        (USED, USED),
        (EXHAUSTED, EXHAUSTED),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    part_number = models.CharField(max_length=100, unique=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    supplier = models.CharField(max_length=100)
    warranty_until = models.DateField(blank=True, null=True)
    available = models.BooleanField(default=True)
    hours_used = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=BRAND_NEW)
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True)