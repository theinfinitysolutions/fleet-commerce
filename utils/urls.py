from django.urls import path

from utils.views import FileObjectView, LocationView

urlpatterns = [
    path("file/<int:pk>/", FileObjectView.as_view(), name="file"),
    path("file/", FileObjectView.as_view(), name="file-create"),
    path("location/", LocationView.as_view(), name="file-create"),
    path("location/<int:pk>/", LocationView.as_view(), name="file-update"),
]
