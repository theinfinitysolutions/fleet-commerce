from django_filters import rest_framework as filters

from .models import WorkOrder

class WorkOrderFilter(filters.FilterSet):
    created_at_gte = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_at_lte = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = WorkOrder
        fields = [
            "created_at",
            "machine",
            "billing_party",
            "site",
            "status"
        ]