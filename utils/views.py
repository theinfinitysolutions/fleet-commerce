from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from accounts.decorators import authenticate_view
from fleet_commerce.mixin import BaseApiMixin
from utils.models import Customer, FileObject, Location

from .serializers import (
    CreateFileSerializer,
    CustomerSerializer,
    FileObjectSerializer,
    LocationSerializer,
)


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
        locations = Location.objects.filter(organisation=request.user.organisation)
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


class CustomerView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            customer = get_object_or_404(Customer, pk=pk)
            serializer = CustomerSerializer(customer)
            return self.successful_get_response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = CustomerSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return self.get_paginated_response([])

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            return self.successful_post_response(CustomerSerializer(file).data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=kwargs.get("pk"))
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)
