from django.db.models.signals import pre_save

from accounts.models import User
from fleet_commerce.middleware import get_current_user
from fleet_commerce.mixin import AuthorTimeStampedModel


def author_handler(instance: AuthorTimeStampedModel, **kwargs):
    if not instance.pk:
        # Instance was created
        user = get_current_user()

        if isinstance(user, User):
            instance.created_by = user


for subclass in AuthorTimeStampedModel.__subclasses__():
    pre_save.connect(author_handler, subclass)
