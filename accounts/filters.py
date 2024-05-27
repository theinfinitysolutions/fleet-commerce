from django_filters import rest_framework as filters

from accounts.models import User


class UserFilter(filters.FilterSet):
    created_at_gte = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_at_lte = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = User
        fields = [
            "created_at",
            "verified",
        ]
