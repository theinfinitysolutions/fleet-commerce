from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Organisation, User
from fleet_commerce.middleware import get_current_organisation, get_current_user
from fleet_commerce.mixin import AuthorTimeStampedModel, OrganisationTimeStampedModel


@receiver(pre_save, sender=AuthorTimeStampedModel)
def author_pre_save_handler(sender, instance, **kwargs):
    if not instance.pk:
        # Instance was created
        user = get_current_user()
        if isinstance(user, User):
            instance.created_by = user


@receiver(pre_save, sender=OrganisationTimeStampedModel)
def organisation_pre_save_handler(sender, instance, **kwargs):
    if not instance.pk:
        organisation = get_current_organisation()
        if isinstance(organisation, Organisation):
            instance.organisation = organisation

        user = get_current_user()
        if isinstance(user, User):
            instance.created_by = user


# Connect signals for all subclasses of AuthorTimeStampedModel
for subclass in AuthorTimeStampedModel.__subclasses__():
    pre_save.connect(author_pre_save_handler, sender=subclass)

# Connect signals for all subclasses of OrganisationTimeStampedModel
for subclass in OrganisationTimeStampedModel.__subclasses__():
    pre_save.connect(organisation_pre_save_handler, sender=subclass)
