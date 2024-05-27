from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import WorkOrderView

urlpatterns = [
    path("workorder/<int:pk>/", WorkOrderView.as_view(), name="workorder-detail"),
    path("workorder/", WorkOrderView.as_view(), name="workorder-create"),
]
