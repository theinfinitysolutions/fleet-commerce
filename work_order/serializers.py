from rest_framework import serializers

from fleet.serializers import MachineSerializer
from billing.serializers import InvoiceSerializer
from accounts.serializers import UserSerializer

from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    Users = serializers.SerializerMethodField()
    Machines = serializers.SerializerMethodField()
    Invoices = serializers.SerializerMethodField()

    def get_users(self, obj):
        users = obj.user_set.filter(is_deleted=False)
        return UserSerializer(users, many=True).data

    def get_machines(self, obj):
        machines = obj.machine_set.filter(is_deleted=False).all()
        return MachineSerializer(machines, many=True).data

    def get_invoices(self, obj):
        invoices = obj.invoices_set.filter(is_deleted=False).all()
        return InvoiceSerializer(invoices, many=True).data

    class Meta:
        model = WorkOrder
        fields = "__all__"  # Adjust fields as necessary
