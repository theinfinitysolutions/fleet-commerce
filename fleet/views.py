from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from accounts.decorators import authenticate_view
from fleet.filters import MachineFilter
from fleet_commerce.mixin import BaseApiMixin
from pagination import StandardResultsPagination

from .models import (
    FitnessDetail,
    InsuranceDetail,
    LoanDetails,
    LocationDetail,
    Machine,
    PUCDetail,
    PurchaseDetails,
    RCBookDetail,
    RoadTaxDetail,
    TyreDetail,
)
from .serializers import (
    FitnessDetailSerializer,
    InsuranceDetailSerializer,
    LoanDetailsSerializer,
    LocationDetailSerializer,
    MachineSerializer,
    PUCDetailSerializer,
    PurchaseDetailsSerializer,
    RCBookDetailSerializer,
    RoadTaxDetailSerializer,
    TyreDetailSerializer,
)


class MachineView(BaseApiMixin, ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MachineFilter
    search_fields = ["machine_number", "engine_number", "chasis_number", "make_and_model"]
    pagination_class = StandardResultsPagination

    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single Machine instance by its ID.
        """
        pk = kwargs.get("pk", None)
        if pk:
            machine = get_object_or_404(Machine, pk=pk)
            serializer = MachineSerializer(machine)
            return self.successful_get_response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = MachineSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return self.get_paginated_response([])

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new Machine instance from provided data.
        """
        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing Machine instance.
        """
        machine = get_object_or_404(Machine, pk=kwargs.get("pk"))

        serializer = MachineSerializer(machine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class PurchaseDetailsView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(PurchaseDetails, pk=kwargs.get("pk"))
        serializer = PurchaseDetailsSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = PurchaseDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(PurchaseDetails, pk=kwargs.get("pk"))
        serializer = PurchaseDetailsSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class LoanDetailsViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(LoanDetails, pk=kwargs.get("pk"))
        serializer = LoanDetailsSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = LoanDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(LoanDetails, pk=kwargs.get("pk"))
        serializer = LoanDetailsSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


# Viewset for LocationDetail
class LocationDetailViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(LocationDetail, pk=kwargs.get("pk"))
        serializer = LocationDetailSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = LocationDetailSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(LocationDetail, pk=kwargs.get("pk"))
        serializer = LocationDetailSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


# Viewset for InsuranceDetail
class InsuranceDetailViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(InsuranceDetail, pk=kwargs.get("pk"))
        serializer = InsuranceDetailSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = InsuranceDetailSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(InsuranceDetail, pk=kwargs.get("pk"))
        serializer = InsuranceDetailSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


# Viewset for TyreDetail
class TyreDetailViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(TyreDetail, pk=kwargs.get("pk"))
        serializer = TyreDetailSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = TyreDetailSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(TyreDetail, pk=kwargs.get("pk"))
        serializer = TyreDetailSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


# Viewset for FitnessDetail
class FitnessDetailViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(FitnessDetail, pk=kwargs.get("pk"))
        serializer = FitnessDetailSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = FitnessDetailSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(FitnessDetail, pk=kwargs.get("pk"))
        serializer = FitnessDetailSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class RoadTaxDetailViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(RoadTaxDetail, pk=kwargs.get("pk"))
        serializer = RoadTaxDetailSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = RoadTaxDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(RoadTaxDetail, pk=kwargs.get("pk"))
        serializer = RoadTaxDetailSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class PUCDetailViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(PUCDetail, pk=kwargs.get("pk"))
        serializer = PUCDetailSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = PUCDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(PUCDetail, pk=kwargs.get("pk"))
        serializer = PUCDetailSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class RCBookDetailViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single PurchaseDetails instance by its ID.
        """
        machine = get_object_or_404(RCBookDetail, pk=kwargs.get("pk"))
        serializer = RCBookDetailSerializer(machine)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def post(self, request, *args, **kwargs):
        """
        Creates a new PurchaseDetails instance from provided data.
        """
        serializer = RCBookDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing PurchaseDetails instance.
        """
        purchase_details = get_object_or_404(RCBookDetail, pk=kwargs.get("pk"))
        serializer = RCBookDetailSerializer(purchase_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)
