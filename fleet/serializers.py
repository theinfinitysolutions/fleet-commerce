from rest_framework import serializers

from utils.mixins import DynamicFieldSerializerMixin
from utils.serializers import FileObjectSerializer
from workorder.models import MachineResourceLinkage, WorkOrder

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


class PurchaseDetailsSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetails
        fields = "__all__"


class LoanDetailsSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = LoanDetails
        fields = "__all__"


class LocationDetailSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = LocationDetail
        fields = "__all__"


class InsuranceDetailSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    insurance_document = serializers.SerializerMethodField()

    def get_insurance_document(self, obj):
        if obj.document:
            return FileObjectSerializer(obj.document).data

    class Meta:
        model = InsuranceDetail
        fields = "__all__"


class TyreDetailSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = TyreDetail
        fields = "__all__"


class FitnessDetailSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = FitnessDetail
        fields = "__all__"


class RoadTaxDetailSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = RoadTaxDetail
        fields = "__all__"


class PUCDetailSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = PUCDetail
        fields = "__all__"


class RCBookDetailSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = RCBookDetail
        fields = "__all__"


class MachineSerializer(DynamicFieldSerializerMixin, serializers.ModelSerializer):
    dynamic_fields = {
        "locations": "with_locations",
        "insurances": "with_insurances",
        "tyres": "with_tyres",
        "fitnesses": "with_fitnesses",
        "purchase_details": "with_purchase_details",
        "loan_details": "with_loan_details",
        "road_tax_detail": "with_road_tax_detail",
        "puc_detail": "with_puc_detail",
        "rc_book_detail": "with_rc_book_detail",
        "work_order": "with_work_order",
    }

    field_serializers = {
        "locations": ("locationdetail_set", "LocationDetailSerializer"),
        "insurances": ("insurancedetail_set", "InsuranceDetailSerializer"),
        "tyres": ("tyredetail_set", "TyreDetailSerializer"),
        "fitnesses": ("fitnessdetail_set", "FitnessDetailSerializer"),
        "purchase_details": ("purchasedetails", "PurchaseDetailsSerializer"),
        "loan_details": ("loandetails", "LoanDetailsSerializer"),
        "road_tax_detail": ("roadtaxdetail", "RoadTaxDetailSerializer"),
        "puc_detail": ("pucdetail", "PUCDetailSerializer"),
        "rc_book_detail": ("rcbookdetail", "RCBookDetailSerializer"),
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
            if related_obj:
                return serializer_class(related_obj, many=many).data

    for field_name, (related_field, serializer_class_name) in field_serializers.items():
        locals()[
            f"get_{field_name}"
        ] = lambda self, obj, rf=related_field, scn=serializer_class_name: self.get_dynamic_field(
            obj, rf, scn
        )

    def get_work_order(self, obj):
        from workorder.serializers import WorkOrderSerializer

        mrl = MachineResourceLinkage.objects.filter(machine=obj)
        wos = WorkOrder.objects.filter(machine_resource_linkage__in=mrl)
        return WorkOrderSerializer(wos, many=True).data

    class Meta:
        model = Machine
        fields = "__all__"  # Adjust fields as necessary
