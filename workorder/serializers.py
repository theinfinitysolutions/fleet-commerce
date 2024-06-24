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
    dynamic_fields = {
        "machine_resource_linkage": "with_machine_resource_linkage",
        "machines": "with_machines",
    }
    billing_details = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    resource_alloted = serializers.SerializerMethodField()

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",  # The ForeignKey relationship
        write_only=True,
    )
    machines = serializers.SerializerMethodField()

    def get_machines(self, obj):
        machine_ids = (
            obj.machine_resource_linkage.filter(is_deleted=False)
            .values_list("machine", flat=True)
            .distinct()
        )
        machines = Machine.objects.filter(id__in=machine_ids).distinct()
        return MachineSerializer(machines, many=True).data

    def get_resource_alloted(self, obj):
        resources = obj.machine_resource_linkage.filter(is_deleted=False).all()
        return MachineResourceLinkageSerializer(resources, many=True).data

    def get_billing_details(self, obj):
        if obj.billing_details:
            invoices = obj.billing_details.filter(is_deleted=False).all()
            return InvoiceSerializer(invoices, many=True).data
        return None

    def get_customer(self, obj):
        customer = obj.customer
        if not customer.is_deleted:
            return CustomerSerializer(customer).data
        return None

    class Meta:
        model = WorkOrder
        fields = "__all__"


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
    machine = MachineSerializer()
    resource = UserSerializer()

    class Meta:
        model = MachineResourceLinkage
        fields = "__all__"
