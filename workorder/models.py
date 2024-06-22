from django.db import models

from accounts.models import User
from billing.models import Invoice
from fleet.models import Machine
from fleet_commerce.mixin import OrganisationTimeStampedModel
from utils.models import Customer


class WorkOrder(OrganisationTimeStampedModel):
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


class DailyUpdate(OrganisationTimeStampedModel):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    shift = models.CharField(max_length=20)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="driver")
    helper = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="helper")
    hmr = models.IntegerField()
    num_moves = models.IntegerField()
    overtime = models.IntegerField(default=0)
    cooling_minutes = models.IntegerField(default=0)
    safety_check_shoes = models.BooleanField(default=True)
    safety_check_jacket = models.BooleanField(default=True)
    safety_check_helmet = models.BooleanField(default=True)


class FitnessReport(OrganisationTimeStampedModel):
    WORKING = "Working"
    NOT_WORKING = "Not Working"

    CAMERA_CONDITION_CHOICES = [
        (WORKING, WORKING),
        (NOT_WORKING, NOT_WORKING),
    ]

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

    BATTERY_WATER_LEVEL_CHOICES = [
        (LOW, LOW),
        (MEDIUM, MEDIUM),
        (HIGH, HIGH),
    ]

    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    fuel_consumed_in_litres = models.IntegerField()
    transmission_oil_in_litres = models.IntegerField()
    hydraulic_oil_in_litres = models.IntegerField()
    brake_oil_in_litres = models.IntegerField()
    engine_oil_in_litres = models.IntegerField()
    tyre_condition = models.CharField(max_length=20)
    camera_condition = models.CharField(max_length=20, choices=CAMERA_CONDITION_CHOICES)
    battery_water_level = models.CharField(max_length=20, choices=BATTERY_WATER_LEVEL_CHOICES)
