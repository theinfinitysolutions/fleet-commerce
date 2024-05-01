from django.db import models

from product.models import TimeStampedModel


class Machine(TimeStampedModel):
    machine_number = models.CharField(max_length=100, unique=True)
    engine_number = models.CharField(max_length=100, blank=True, null=True)
    chasis_number = models.CharField(max_length=100, blank=True, null=True)
    make_and_model = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    registration_rto_office = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField()
    valid_upto = models.DateField()
    registered_owner = models.CharField(max_length=100, blank=True, null=True)
    account_billing_hirer_company = models.CharField(max_length=100, blank=True, null=True)
    asset_type = models.CharField(max_length=100, blank=True, null=True)
    machine_type = models.CharField(max_length=100, blank=True, null=True)
    vehicle_image = models.ForeignKey("utils.FileObject", null=True, on_delete=models.SET_NULL)


class PurchaseDetails(TimeStampedModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE)
    bill_no = models.CharField(max_length=100)
    bill_date = models.DateField()
    total_bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_name = models.CharField(max_length=100)
    taxable_amount_18_percent = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    cgst_18_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sgst_18_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    igst_18_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    taxable_amount_28_percent = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    cgst_28_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sgst_28_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    igst_28_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class LoanDetails(TimeStampedModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE)
    purchased_on_loan = models.BooleanField(default=False)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    loan_account_number = models.CharField(max_length=100, blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loan_tenure_from = models.DateField()
    loan_tenure_to = models.DateField()
    installment_date = models.DateField()
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    number_of_installments = models.IntegerField(blank=True, null=True)


class LocationDetail(TimeStampedModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    from_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)


class InsuranceDetail(TimeStampedModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    insurance_company = models.CharField(max_length=100, blank=True, null=True)
    policy_number = models.CharField(max_length=100, blank=True, null=True)
    policy_start_date = models.DateField()
    policy_end_date = models.DateField()
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    insurance_type = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


class TyreDetail(TimeStampedModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    tyre_number = models.CharField(max_length=100, blank=True, null=True)
    from_date = models.DateField()
    meter_reading = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


class FitnessDetail(TimeStampedModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    fitness_certificate_number = models.CharField(max_length=100, blank=True, null=True)
    fitness_certificate_date = models.DateField()
    fitness_certificate_expiry_date = models.DateField()
    fitness_certificate_remarks = models.TextField(blank=True, null=True)
    fitness_document_links = models.JSONField(
        blank=True, null=True
    )  # This field requires Django 3.1 or newer


class RoadTaxDetail(TimeStampedModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE)
    road_tax_permit_number = models.CharField(max_length=100, blank=True, null=True)
    road_tax_from_date = models.DateField()
    road_tax_to_date = models.DateField()
    road_tax_remarks = models.TextField(blank=True, null=True)


class PUCDetail(TimeStampedModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE)
    puc_number = models.CharField(max_length=100, blank=True, null=True)
    puc_from_date = models.DateField()
    puc_to_date = models.DateField()
    puc_remarks = models.TextField(blank=True, null=True)


class RCBookDetail(TimeStampedModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE)
    rc_book_number = models.CharField(max_length=100, blank=True, null=True)
    rc_book_from_date = models.DateField()
    rc_book_to_date = models.DateField()
    rc_book_remarks = models.TextField(blank=True, null=True)
