from django.urls import path

from utils.views import FileObjectView

urlpatterns = [
    path("file/<int:pk>/", FileObjectView.as_view(), name="file"),
    path("file/", FileObjectView.as_view(), name="file-create"),
]
