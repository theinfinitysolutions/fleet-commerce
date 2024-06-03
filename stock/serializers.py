from rest_framework import serializers

from workorder.serializers import WorkOrderSerializer
from fleet.serializers import MachineSerializer


from workorder.models import WorkOrder
from fleet.models import Machine
from .models import SparePart

class SparePartSerializer(serializers.ModelSerializer):
    work_order = serializers.SerializerMethodField()
    machine = serializers.SerializerMethodField()

    work_order_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkOrder.objects.all(),
        source='work_order',
        write_only=True
    )

    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(),
        source='machine',
        write_only=True
    )

    def get_work_order(self, obj):
        work_order = obj.work_order
        if not work_order or work_order.is_deleted:
            return None
        return WorkOrderSerializer(work_order).data
    
    def get_machine(self, obj):
        machine = obj.machine
        if not machine or machine.is_deleted:
            return None
        return MachineSerializer(machine).data

    class Meta:
        model = SparePart
        fields = "__all__"
