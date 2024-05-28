from rest_framework import serializers

from billing.serializers import InvoiceSerializer
from fleet.serializers import MachineSerializer
from accounts.serializers import UserSerializer
from utils.serializers import CustomerSerializer

from .models import WorkOrder
from fleet.models import Machine
from accounts.models import User
from utils.models import Customer

class WorkOrderSerializer(serializers.ModelSerializer):
    machines = serializers.PrimaryKeyRelatedField(many=True, queryset=Machine.objects.all())
    invoices = serializers.SerializerMethodField()
    resource_details = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    def get_invoices(self, obj):
        invoices = obj.invoices_set.filter(is_deleted=False).all()
        return InvoiceSerializer(invoices, many=True).data

    class Meta:
        model = WorkOrder
        fields = "__all__"  # Adjust fields as necessary
