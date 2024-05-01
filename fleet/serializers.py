from rest_framework import serializers

from utils.serializers import FileObjectSerializer

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


class PurchaseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetails
        fields = "__all__"


class LoanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDetails
        fields = "__all__"


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetail
        fields = "__all__"


class InsuranceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceDetail
        fields = "__all__"


class TyreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TyreDetail
        fields = "__all__"


class FitnessDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessDetail
        fields = "__all__"


class RoadTaxDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadTaxDetail
        fields = "__all__"


class PUCDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PUCDetail
        fields = "__all__"


class RCBookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RCBookDetail
        fields = "__all__"


class MachineSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    insurance = serializers.SerializerMethodField()
    tyre = serializers.SerializerMethodField()
    fitness = serializers.SerializerMethodField()
    vehicle_image = serializers.SerializerMethodField()
    purchase_details = serializers.SerializerMethodField()
    loan_details = serializers.SerializerMethodField()
    puc_details = serializers.SerializerMethodField()
    rc_book_details = serializers.SerializerMethodField()

    def get_location(self, obj):
        locations = obj.locationdetail_set.filter(is_deleted=False).all()
        return LocationDetailSerializer(locations, many=True).data

    def get_insurance(self, obj):
        insurances = obj.insurancedetail_set.filter(is_deleted=False).all()
        return InsuranceDetailSerializer(insurances, many=True).data

    def get_tyre(self, obj):
        tyres = obj.tyredetail_set.filter(is_deleted=False).all()
        return TyreDetailSerializer(tyres, many=True).data

    def get_fitness(self, obj):
        fitnesses = obj.fitnessdetail_set.filter(is_deleted=False).all()
        return FitnessDetailSerializer(fitnesses, many=True).data

    def get_purchase_details(self, obj):
        purchasedetails = obj.purchasedetails
        if purchasedetails:
            return PurchaseDetailsSerializer(purchasedetails).data

    def get_loan_details(self, obj):
        if hasattr(obj, "loandetails"):
            loandetails = obj.loandetails
            return LoanDetailsSerializer(loandetails).data

    def get_puc_details(self, obj):
        if hasattr(obj, "pucdetails"):
            pucdetails = obj.pucdetails
            return PUCDetailSerializer(pucdetails).data

    def get_rc_book_details(self, obj):
        if hasattr(obj, "rcbookdetails"):
            rcbookdetails = obj.rcbookdetails
            return RCBookDetailSerializer(rcbookdetails).data

    def get_vehicle_image(self, obj):
        if obj.vehicle_image:
            return FileObjectSerializer(obj.vehicle_image).data

    class Meta:
        model = Machine
        fields = "__all__"  # Adjust fields as necessary
