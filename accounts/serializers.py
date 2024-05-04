from rest_framework import serializers

from .models import User,DocumentDetails,BankDetails

class UserSerializer(serializers.ModelSerializer):
    documentdetails = serializers.SerializerMethodField()
    bankdetails = serializers.SerializerMethodField()

    def get_documentdetails(self, obj):
        return DocumentDetailsSerializer(obj.documentdetails_set.all(), many=True).data
    
    def get_bankdetails(self, obj):
        return BankDetailsSerializer(obj.bankdetails_set.all(), many=True).data

    class Meta:
        model = User
        fields = '__all__'

class DocumentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentDetails
        fields = '__all__'

class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'