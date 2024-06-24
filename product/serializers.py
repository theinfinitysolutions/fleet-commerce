from rest_framework import serializers

from utils.mixins import DynamicFieldSerializerMixin

from .models import (
    Contract,
    DailyAttendance,
    IssueReport,
    Product,
    ReadingTransaction,
    Reimbursement,
)


class ProductSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ContractSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class ReadingTransactionSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ReadingTransaction
        fields = "__all__"


class DailyAttendanceSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = DailyAttendance
        fields = "__all__"


class ReimbursementSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Reimbursement
        fields = "__all__"


class IssueReportSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = IssueReport
        fields = "__all__"
