from rest_framework import serializers

from billing.serializers import InvoiceSerializer
from fleet.serializers import MachineSerializer
from accounts.serializers import UserSerializer
from utils.serializers import CustomerSerializer

from .models import WorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    machines = serializers.SerializerMethodField()
    invoices = serializers.SerializerMethodField()
    resource_details = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    def get_machines(self, obj):
        machines = obj.machines.filter(is_deleted=False).all()
        return MachineSerializer(machines, many=True).data

    def get_invoices(self, obj):
        invoices = obj.invoices_set.filter(is_deleted=False).all()
        return InvoiceSerializer(invoices, many=True).data

    def get_resource_details(self, obj):
        resources = obj.resource_details.filter(is_deleted=False).all()
        return UserSerializer(resources, many=True).data

    def get_customer(self, obj):
        customer = obj.customer_set.filter(is_deleted=False).all()
        return CustomerSerializer(customer, many=True).data
        
    class Meta:
        model = WorkOrder
        fields = "__all__"  # Adjust fields as necessary
