from django_filters import rest_framework as filters

from fleet.models import Machine


class MachineFilter(filters.FilterSet):
    created_at_gte = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_at_lte = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Machine
        fields = [
            "created_at",
            "machine_number",
            "make_and_model",
            "year",
            "asset_type",
            "machine_type",
        ]
