from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from accounts.decorators import authenticate_view
from fleet_commerce.mixin import BaseApiMixin
from pagination import StandardResultsPagination

from .filters import WorkOrderFilter
from .models import WorkOrder
from .serializers import WorkOrderSerializer


class WorkOrderView(BaseApiMixin, ListAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = WorkOrderFilter
    search_fields = ["billing_party", "machine", "site", "status"]
    pagination_class = StandardResultsPagination

    @authenticate_view
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single WorkOrder instance by its ID.
        """
        pk = kwargs.get("pk", None)
        if pk:
            WorkOrder = get_object_or_404(WorkOrder, pk=pk)
            serializer = WorkOrderSerializer(WorkOrder)
            return self.successful_get_response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = WorkOrderSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return self.get_paginated_response([])

    @authenticate_view
    def post(self, request, *args, **kwargs):
        """
        Creates a new WorkOrder instance from provided data.
        """
        serializer = WorkOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing WorkOrder instance.
        """
        WorkOrder = get_object_or_404(WorkOrder, pk=kwargs.get("pk"))

        serializer = WorkOrderSerializer(WorkOrder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)
