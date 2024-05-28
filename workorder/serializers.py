from rest_framework import serializers

from billing.serializers import InvoiceSerializer
from fleet.serializers import MachineSerializer
from accounts.serializers import UserSerializer
from utils.serializers import CustomerSerializer

from .models import WorkOrder
from fleet.models import Machine
from utils.models import Customer
from accounts.models import User

class WorkOrderSerializer(serializers.ModelSerializer):
    machines = serializers.SerializerMethodField()
    invoices = serializers.SerializerMethodField()
    resource_details = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    machine_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Machine.objects.all(),
        source='machine',  # Linking directly to the many-to-many field on the model
        write_only=True
    )

    resource_detail_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        source='resource_details',  # Linking directly to the many-to-many field on the model
        write_only=True
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',  # The ForeignKey relationship
        write_only=True
    )

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
