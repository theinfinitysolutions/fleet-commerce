from rest_framework import serializers

from utils.mixins import DynamicFieldSerializerMixin

from .models import Invoice


class InvoiceSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"
