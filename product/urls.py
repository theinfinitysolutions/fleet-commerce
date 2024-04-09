from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'contracts', views.ContractViewSet)
router.register(r'readingtransactions', views.ReadingTransactionViewSet)
router.register(r'dailyattendances', views.DailyAttendanceViewSet)
router.register(r'reimbursements', views.ReimbursementViewSet)
router.register(r'issuereports', views.IssueReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
