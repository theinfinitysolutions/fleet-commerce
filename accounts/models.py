from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.serializers import ValidationError

from fleet_commerce.mixin import AuthorTimeStampedModel, TimeStampedModel


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


class User(AbstractUser, TimeStampedModel):
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
    organisation = models.ForeignKey("accounts.Organisation", on_delete=models.SET_NULL, null=True)
    roles = models.ManyToManyField("accounts.Role", through="UserRole")

    def direct_roles(self):
        return self.roles.only("name").values_list("name", flat=True)

    def has_role(self, role):
        """
        Check if the user is assigned a role or not.
        A DB query is fired every time this method is called, see if caching is required.
        """
        available_roles = self.direct_roles()

        if role in available_roles:
            return True

        for available_role in available_roles:
            if role in Role.all_roles(available_role):
                return True

        return False

    def assign_role(self, role_name):
        role = Role.objects.filter(name=role_name).first()
        if not role:
            raise ValidationError({"role": "Role does not exist."})
        UserRole.objects.get_or_create(user_id=self.id, role_id=role.id)

    def revoke_role(self, role_name):
        role = Role.objects.filter(name=role_name).first()
        if not role:
            raise ValidationError({"role": "Role does not exist."})
        UserRole.objects.filter(user_id=self.id, role_id=role.id).delete()


class Organisation(AuthorTimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, null=True)
    contact_person = models.CharField(max_length=100, null=True)
    contact_email = models.EmailField(null=True)
    contact_phone_number = models.CharField(max_length=17, null=True)
    website = models.URLField(null=True)
    description = models.TextField(null=True)


class Role(TimeStampedModel):
    SUPER_ADMIN = "super_admin"
    ORGANISATION_ADMIN = "organisation_admin"
    VENDOR = "vendor"

    USER_ROLE_CHOICES = (
        (SUPER_ADMIN, SUPER_ADMIN),
        (ORGANISATION_ADMIN, ORGANISATION_ADMIN),
        (VENDOR, VENDOR),
    )

    ROLE_HIERARCHY = {
        SUPER_ADMIN: [ORGANISATION_ADMIN],
        ORGANISATION_ADMIN: [VENDOR],
    }

    name = models.CharField(max_length=50, choices=USER_ROLE_CHOICES)

    class Meta:
        indexes = [models.Index(fields=["name"])]

    @staticmethod
    def all_roles(role):
        """
        Returns all sub-roles for a role.
        """
        roles = set([role])
        for child_role in Role.ROLE_HIERARCHY.get(role, []):
            roles = roles.union(Role.all_roles(child_role))

        return list(roles)

    def __str__(self):
        return f"{self.name} <{self.id}>"


class UserRole(TimeStampedModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
