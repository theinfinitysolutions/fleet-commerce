from django.urls import path

from utils.views import FileObjectView, LocationView, CustomerView

urlpatterns = [
    path("file/<int:pk>/", FileObjectView.as_view(), name="file"),
    path("file/", FileObjectView.as_view(), name="file-create"),
    path("location/", LocationView.as_view(), name="location"),
    path("location/<int:pk>/", LocationView.as_view(), name="location-update"),
    path("customer/", CustomerView.as_view(), name="customer"),
    path("customer/<int:pk>/", CustomerView.as_view(), name="customer-update"),
]
