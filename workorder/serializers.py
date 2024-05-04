from rest_framework import serializers

from billing.serializers import InvoiceSerializer
from fleet.serializers import MachineSerializer

from .models import WorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    machines = serializers.SerializerMethodField()
    invoices = serializers.SerializerMethodField()

    def get_machines(self, obj):
        machines = obj.machine_set.filter(is_deleted=False).all()
        return MachineSerializer(machines, many=True).data

    def get_invoices(self, obj):
        invoices = obj.invoices_set.filter(is_deleted=False).all()
        return InvoiceSerializer(invoices, many=True).data

    class Meta:
        model = WorkOrder
        fields = "__all__"  # Adjust fields as necessary
