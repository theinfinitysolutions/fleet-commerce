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
    location_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=LocationDetail.objects.all(),
        source="locations",
        required=False,
    )
    insurance_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=InsuranceDetail.objects.all(),
        source="insurances",
        required=False,
    )
    tyre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TyreDetail.objects.all(),
        source="tyres",
        required=False,
    )
    fitness_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FitnessDetail.objects.all(),
        source="fitnesses",
        required=False,
    )
    vehicle_image = serializers.SerializerMethodField()

    def get_vehicle_image(self, obj):
        if obj.vehicle_image:
            return FileObjectSerializer(obj.vehicle_image).data

    class Meta:
        model = Machine
        fields = "__all__"  # Adjust fields as necessary

    def create(self, validated_data):
        # Extract M2M fields data before creation
        locations_data = validated_data.pop("locations", [])
        insurances_data = validated_data.pop("insurances", [])
        tyres_data = validated_data.pop("tyres", [])
        fitnesses_data = validated_data.pop("fitnesses", [])

        # Create the Machine instance without M2M data
        machine = Machine.objects.create(**validated_data)

        # Set M2M relationships after the Machine instance is created
        if locations_data:
            machine.locations.set(locations_data)
        if insurances_data:
            machine.insurances.set(insurances_data)
        if tyres_data:
            machine.tyres.set(tyres_data)
        if fitnesses_data:
            machine.fitnesses.set(fitnesses_data)

        return machine


def update(self, instance, validated_data):
    # Check and update M2M fields only if they are included in the request data
    if "locations" in validated_data:
        locations_data = validated_data.pop("locations")
        instance.locations.set(locations_data)

    if "insurances" in validated_data:
        insurances_data = validated_data.pop("insurances")
        instance.insurances.set(insurances_data)

    if "tyres" in validated_data:
        tyres_data = validated_data.pop("tyres")
        instance.tyres.set(tyres_data)

    if "fitnesses" in validated_data:
        fitnesses_data = validated_data.pop("fitnesses")
        instance.fitnesses.set(fitnesses_data)

    # Update other fields
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()

    return instance
