from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import WorkOrderView, DailyUpdateView, FitnessReportView

urlpatterns = [
    path("workorder/<int:pk>/", WorkOrderView.as_view(), name="workorder-detail"),
    path("workorder/", WorkOrderView.as_view(), name="workorder-create"),
    path("dailyupdate/<int:pk>/", DailyUpdateView.as_view(), name="dailyupdate-detail"),
    path("dailyupdate/", DailyUpdateView.as_view(), name="dailyupdate-create"),
    path("fitnessreport/<int:pk>/", FitnessReportView.as_view(), name="fitnessreport-detail"),
    path("fitnessreport/", FitnessReportView.as_view(), name="fitnessreport-create"),
]
