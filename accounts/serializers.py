from rest_framework import serializers

from accounts.models import BankDetails, DocumentDetails, User
from utils.serializers import FileObjectSerializer


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = "__all__"

    def validate_bank_account_number(self, value):
        # Add your validation logic for bank account number here
        return value

    def validate_ifsc_code(self, value):
        # Add your validation logic for IFSC code here
        return value


class DocumentDetailsSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    def get_document(self, obj):
        if obj.document:
            return FileObjectSerializer(obj.document).data

    class Meta:
        model = DocumentDetails
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    bank_details = BankDetailsSerializer(many=True)
    document_details = DocumentDetailsSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "bank_details", "document_details"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
