from rest_framework import serializers

from .models import User,DocumentDetails,BankDetails,Organization,OrganizationRole,OrganizationPermission

class UserSerializer(serializers.ModelSerializer):
    documentdetails = serializers.SerializerMethodField()
    bankdetails = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_documentdetails(self, obj):
        documentdetails = obj.documentdetails_set.filter(is_deleted=False).all()
        return DocumentDetailsSerializer(documentdetails, many=True).data
    
    def get_bankdetails(self, obj):
        bankdetails = obj.bankdetails_set.filter(is_deleted=False).all()
        return BankDetailsSerializer(bankdetails, many=True).data
    
    def get_organization(self, obj):
        organization = obj.organization_set.filter(is_deleted=False).all()
        return OrganizationSerializer(organization).data
    
    def get_role(self, obj):
        role = obj.organizationrole_set.filter(is_deleted=False).all()
        return OrganizationRoleSerializer(role, many=True).data

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

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        extra_kwargs = {
            'is_deleted': {'read_only': False}
        }

    def create(self, validated_data):
        organization = Organization.objects.create(**validated_data)
        role = OrganizationRole.objects.create(organization=organization, role="ADMIN")
        permissions = OrganizationRole.objects.create(role=role, permission="ALL")
        user = User.objects.get(pk = organization.created_by_id)
        User.objects.filter(id=user.id).update(organization=organization,role=role)
        return organization

class OrganizationRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationRole
        fields = '__all__'

class OrganizationPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationPermission
        fields = '__all__'