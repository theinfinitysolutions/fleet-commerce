from rest_framework import viewsets

from .models import (
    Contract,
    DailyAttendance,
    IssueReport,
    Product,
    ReadingTransaction,
    Reimbursement,
)
from .serializers import (
    ContractSerializer,
    DailyAttendanceSerializer,
    IssueReportSerializer,
    ProductSerializer,
    ReadingTransactionSerializer,
    ReimbursementSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ReadingTransactionViewSet(viewsets.ModelViewSet):
    queryset = ReadingTransaction.objects.all()
    serializer_class = ReadingTransactionSerializer


class DailyAttendanceViewSet(viewsets.ModelViewSet):
    queryset = DailyAttendance.objects.all()
    serializer_class = DailyAttendanceSerializer


class ReimbursementViewSet(viewsets.ModelViewSet):
    queryset = Reimbursement.objects.all()
    serializer_class = ReimbursementSerializer


class IssueReportViewSet(viewsets.ModelViewSet):
    queryset = IssueReport.objects.all()
    serializer_class = IssueReportSerializer
