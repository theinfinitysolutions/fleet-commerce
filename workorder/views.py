from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from accounts.decorators import authenticate_view
from accounts.models import User
from fleet.models import Machine
from fleet_commerce.mixin import BaseApiMixin
from pagination import StandardResultsPagination

from .filters import WorkOrderFilter
from .models import DailyUpdate, FitnessReport, MachineResourceLinkage, WorkOrder
from .serializers import (
    DailyUpdateSerializer,
    FitnessReportSerializer,
    MachineResourceLinkageSerializer,
    WorkOrderSerializer,
)


class WorkOrderView(BaseApiMixin, ListAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = WorkOrderFilter
    search_fields = ["customer", "machine", "site", "status"]
    pagination_class = StandardResultsPagination

    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single WorkOrder instance by its ID.
        """
        pk = kwargs.get("pk", None)
        if pk:
            work_order = get_object_or_404(WorkOrder, pk=pk)
            serializer = WorkOrderSerializer(work_order, context=request.query_params)
            return self.successful_get_response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = WorkOrderSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return self.get_paginated_response([])

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new WorkOrder instance from provided data.
        """
        serializer = WorkOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing WorkOrder instance.
        """
        work_order = get_object_or_404(WorkOrder, pk=kwargs.get("pk"))

        serializer = WorkOrderSerializer(work_order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class AddWorkOrderMachineResource(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Adds a new MachineResourceLinkage instance from provided data.
        """
        work_order = get_object_or_404(WorkOrder, pk=request.data.get("work_order"))
        machine = get_object_or_404(Machine, pk=request.data.get("machine"))
        resource = get_object_or_404(User, pk=request.data.get("resource"))

        linkage = MachineResourceLinkage.objects.create(machine=machine, resource=resource)
        work_order.machine_resource_linkage.add(linkage)
        serializer = MachineResourceLinkageSerializer(linkage)
        return self.successful_post_response(serializer.data)


class DailyUpdateView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single DailyUpdate instance by its ID.
        """
        if "pk" in kwargs:
            daily_update = get_object_or_404(DailyUpdate, pk=kwargs.get("pk"))
            serializer = DailyUpdateSerializer(daily_update)
        else:
            daily_update = DailyUpdate.objects.filter(organisation=request.user.organisation)
            serializer = DailyUpdateSerializer(daily_update, many=True)

        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new DailyUpdate instance from provided data.
        """
        serializer = DailyUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing DailyUpdate instance.
        """
        daily_update = get_object_or_404(DailyUpdate, pk=kwargs.get("pk"))

        serializer = DailyUpdateSerializer(daily_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class FitnessReportView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single FitnessReport instance by its ID.
        """
        if "pk" in kwargs:
            fitness_report = get_object_or_404(FitnessReport, pk=kwargs.get("pk"))
            serializer = FitnessReportSerializer(fitness_report)
        else:
            fitness_report = FitnessReport.objects.filter(organisation=request.user.organisation)
            serializer = FitnessReportSerializer(fitness_report, many=True)

        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new FitnessReport instance from provided data.
        """
        serializer = FitnessReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing FitnessReport instance.
        """
        fitness_report = get_object_or_404(FitnessReport, pk=kwargs.get("pk"))

        serializer = FitnessReportSerializer(fitness_report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)
