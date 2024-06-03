from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SparePartView

urlpatterns = [
    path("stock/<int:pk>/", SparePartView.as_view(), name="sparepart-detail"),
    path("stock/", SparePartView.as_view(), name="sparepart-create"),
]
