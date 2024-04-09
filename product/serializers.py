from rest_framework import serializers
from .models import Product, Contract, ReadingTransaction, DailyAttendance, Reimbursement, IssueReport

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class ReadingTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingTransaction
        fields = '__all__'

class DailyAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAttendance
        fields = '__all__'

class ReimbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reimbursement
        fields = '__all__'

class IssueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueReport
        fields = '__all__'
