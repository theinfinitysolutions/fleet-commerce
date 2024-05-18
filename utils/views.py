from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from accounts.decorators import authenticate_view
from fleet_commerce.mixin import BaseApiMixin
from utils.models import FileObject, Location

from .serializers import CreateFileSerializer, FileObjectSerializer, LocationSerializer


class FileObjectView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        machine = get_object_or_404(FileObject, pk=kwargs.get("pk"))
        serializer = FileObjectSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        serializer = CreateFileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            return self.successful_post_response(FileObjectSerializer(file).data)
        return self.error_response(errors=serializer.errors)


class LocationView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        locations = Location.objects.filter(organisation=request.organisation)
        serializer = LocationSerializer(locations, many=True)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            return self.successful_post_response(LocationSerializer(file).data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        location = get_object_or_404(Location, pk=kwargs.get("pk"))
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)
