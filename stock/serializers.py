from rest_framework import serializers

from fleet.models import Machine
from fleet.serializers import MachineSerializer
from utils.mixins import DynamicFieldSerializerMixin
from workorder.models import WorkOrder
from workorder.serializers import WorkOrderSerializer

from .models import SparePart


class SparePartSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    work_order_obj = serializers.SerializerMethodField()
    machine_obj = serializers.SerializerMethodField()

    def get_work_order_obj(self, obj):
        work_order = obj.work_order
        if not work_order or work_order.is_deleted:
            return None
        return WorkOrderSerializer(work_order).data

    def get_machine_obj(self, obj):
        machine = obj.machine
        if not machine or machine.is_deleted:
            return None
        return MachineSerializer(machine).data

    class Meta:
        model = SparePart
        fields = "__all__"
