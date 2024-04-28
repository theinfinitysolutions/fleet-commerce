from django.urls import path
from rest_framework.routers import DefaultRouter

from fleet.views import (
    FitnessDetailViewSet,
    InsuranceDetailViewSet,
    LoanDetailsViewSet,
    LocationDetailViewSet,
    MachineView,
    PUCDetailViewSet,
    PurchaseDetailsView,
    RCBookDetailViewSet,
    RoadTaxDetailViewSet,
    TyreDetailViewSet,
)

urlpatterns = [
    path("machines/<int:pk>/", MachineView.as_view(), name="machine-detail"),
    path("machines/", MachineView.as_view(), name="machine-create"),
    path("purchase-details/<int:pk>/", PurchaseDetailsView.as_view(), name="purchase-detail"),
    path("purchase-details/", PurchaseDetailsView.as_view(), name="purchase-create"),
    path("loan-detials/<int:pk>/", LoanDetailsViewSet.as_view(), name="loan-detail"),
    path("loan-detials/", LoanDetailsViewSet.as_view(), name="loan-create"),
    path("location-details/<int:pk>/", LocationDetailViewSet.as_view(), name="location-detail"),
    path("location-details/", LocationDetailViewSet.as_view(), name="location-create"),
    path("insurance-details/<int:pk>/", InsuranceDetailViewSet.as_view(), name="insurance-detail"),
    path("insurance-details/", InsuranceDetailViewSet.as_view(), name="insurance-create"),
    path("tyre-detail/<int:pk>/", TyreDetailViewSet.as_view(), name="tyre-detail"),
    path("tyre-detail/", TyreDetailViewSet.as_view(), name="tyre-create"),
    path("fitness-detail/<int:pk>/", FitnessDetailViewSet.as_view(), name="fitness-detail"),
    path("fitness-detail/", FitnessDetailViewSet.as_view(), name="fitness-create"),
    path("road-tax-detail/<int:pk>/", RoadTaxDetailViewSet.as_view(), name="road-tax-detail"),
    path("road-tax-detail/", RoadTaxDetailViewSet.as_view(), name="road-tax-create"),
    path("puc-detail/<int:pk>/", PUCDetailViewSet.as_view(), name="puc-detail"),
    path("puc-detail/", PUCDetailViewSet.as_view(), name="puc-create"),
    path("rc-book-detail/<int:pk>/", RCBookDetailViewSet.as_view(), name="rc-book-detail"),
    path("rc-book-tax-detail/", RCBookDetailViewSet.as_view(), name="rc-book-create"),
]
