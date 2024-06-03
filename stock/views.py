from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from accounts.decorators import authenticate_view
from fleet_commerce.mixin import BaseApiMixin
from pagination import StandardResultsPagination

from .filters import SparePartFilter
from .models import SparePart
from .serializers import SparePartSerializer


class SparePartView(BaseApiMixin, ListAPIView):
    queryset = SparePart.objects.all()
    serializer_class = SparePartSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SparePartFilter
    search_fields = ["work_order", "machine"]
    pagination_class = StandardResultsPagination

    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single SparePart instance by its ID.
        """
        pk = kwargs.get("pk", None)
        if pk:
            spare_part = get_object_or_404(SparePart, pk=pk)
            serializer = SparePartSerializer(spare_part)
            return self.successful_get_response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = SparePartSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return self.get_paginated_response([])

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new SparePart instance from provided data.
        """
        serializer = SparePartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing SparePart instance.
        """
        spare_part = get_object_or_404(SparePart, pk=kwargs.get("pk"))

        serializer = SparePartSerializer(spare_part, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)
