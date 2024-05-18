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
    document = serializers.SerializerMethodField()

    def get_document(self, obj):
        if obj.document:
            return FileObjectSerializer(obj.document).data

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
    field_serializers = {
        "locations": ("locationdetail_set", "LocationDetailSerializer"),
        "insurances": ("insurancedetail_set", "InsuranceDetailSerializer"),
        "tyres": ("tyredetail_set", "TyreDetailSerializer"),
        "fitnesses": ("fitnessdetail_set", "FitnessDetailSerializer"),
        "purchase_details": ("purchasedetails", "PurchaseDetailsSerializer"),
        "loan_details": ("loandetails", "LoanDetailsSerializer"),
        "road_tax_detail": ("roadtaxdetail", "RoadTaxDetailSerializer"),
        "puc_details": ("pucdetails", "PUCDetailSerializer"),
        "rc_book_details": ("rcbookdetails", "RCBookDetailSerializer"),
        "vehicle_image_object": ("vehicle_image", "FileObjectSerializer"),
    }

    for field_name, (related_field, serializer_class_name) in field_serializers.items():
        locals()[field_name] = serializers.SerializerMethodField()

    def get_dynamic_field(self, obj, related_field, serializer_class_name):
        if hasattr(obj, related_field):
            related_obj = getattr(obj, related_field)
            if isinstance(related_obj, (list, tuple)) or hasattr(related_obj, "all"):
                related_obj = related_obj.filter(is_deleted=False).all()
                many = True
            else:
                many = False
            serializer_class = globals()[serializer_class_name]
            return serializer_class(related_obj, many=many).data

    for field_name, (related_field, serializer_class_name) in field_serializers.items():
        locals()[
            f"get_{field_name}"
        ] = lambda self, obj, rf=related_field, scn=serializer_class_name: self.get_dynamic_field(
            obj, rf, scn
        )

    class Meta:
        model = Machine
        fields = "__all__"  # Adjust fields as necessary
