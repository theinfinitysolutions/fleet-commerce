import inspect

from django.db.models import Manager


def apply_is_deleted_filter(queryset):
    return queryset.filter(is_deleted=False)


def should_apply_is_deleted_filter(model_class):
    from fleet_commerce.mixin import IsDeletedMixin

    return IsDeletedMixin in inspect.getmro(model_class)  # or hasattr(model_class, "is_deleted")


class IsDeletedManager(Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        if should_apply_is_deleted_filter(self.model):
            queryset = apply_is_deleted_filter(queryset)
        return queryset
