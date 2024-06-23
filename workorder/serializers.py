from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from billing.serializers import InvoiceSerializer
from fleet.models import Machine
from fleet.serializers import MachineSerializer
from utils.mixins import DynamicFieldSerializerMixin
from utils.models import Customer
from utils.serializers import CustomerSerializer

from .models import DailyUpdate, FitnessReport, MachineResourceLinkage, WorkOrder


class WorkOrderSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    machine = serializers.SerializerMethodField()
    billing_details = serializers.SerializerMethodField()
    resource_details = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    resource_alloted = serializers.SerializerMethodField()

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",  # The ForeignKey relationship
        write_only=True,
    )

    def get_resource_alloted(self, obj):
        resources = obj.machine_resource_linkage.filter(is_deleted=False).all()
        return MachineResourceLinkageSerializer(resources, many=True).data

    def get_machine(self, obj):
        machine = obj.machine.filter(is_deleted=False).all()
        return MachineSerializer(machine, many=True).data

    def get_billing_details(self, obj):
        if obj.billing_details:
            invoices = obj.billing_details.filter(is_deleted=False).all()
            return InvoiceSerializer(invoices, many=True).data
        return None

    def get_resource_details(self, obj):
        resources = obj.resource_details.filter(is_deleted=False).all()
        return UserSerializer(resources, many=True).data

    def get_customer(self, obj):
        customer = obj.customer
        if not customer.is_deleted:
            return CustomerSerializer(customer).data
        return None

    class Meta:
        model = WorkOrder
        fields = "__all__"  # Adjust fields as necessary


class DailyUpdateSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    work_order = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    helper = serializers.SerializerMethodField()

    work_order_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkOrder.objects.all(),
        source="work_order",  # The ForeignKey relationship
        write_only=True,
    )

    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="driver", write_only=True  # The ForeignKey relationship
    )

    helper_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="helper", write_only=True  # The ForeignKey relationship
    )

    def get_work_order(self, obj):
        work_order = obj.work_order
        if not work_order.is_deleted:
            return WorkOrderSerializer(work_order).data
        return None

    def get_driver(self, obj):
        driver = obj.driver
        if not driver or not driver.is_deleted:
            return UserSerializer(driver).data
        return None

    def get_helper(self, obj):
        helper = obj.helper
        if not helper or not helper.is_deleted:
            return UserSerializer(helper).data
        return None

    class Meta:
        model = DailyUpdate
        fields = "__all__"


class FitnessReportSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    work_order = serializers.SerializerMethodField()
    machine = serializers.SerializerMethodField()

    work_order_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkOrder.objects.all(),
        source="work_order",  # The ForeignKey relationship
        write_only=True,
    )

    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(),
        source="machine",  # The ForeignKey relationship
        write_only=True,
    )

    def get_work_order(self, obj):
        work_order = obj.work_order
        if not work_order.is_deleted:
            return WorkOrderSerializer(work_order).data
        return None

    def get_machine(self, obj):
        machine = obj.machine
        if not machine.is_deleted:
            return MachineSerializer(machine).data
        return None

    class Meta:
        model = FitnessReport
        fields = "__all__"


class MachineResourceLinkageSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    resource = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MachineResourceLinkage
        fields = "__all__"
