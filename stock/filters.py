from django_filters import rest_framework as filters

from .models import SparePart

class SparePartFilter(filters.FilterSet):
    created_at_gte = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_at_lte = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = SparePart
        fields = ["available", "status", "category"]
