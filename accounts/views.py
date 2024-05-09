from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView


from fleet_commerce.mixin import BaseApiMixin
from pagination import StandardResultsPagination
from .decorators import authenticate_view, check_permissions
from .serializers import UserSerializer,DocumentDetailsSerializer,BankDetailsSerializer,OrganizationSerializer,OrganizationRoleSerializer,OrganizationPermissionSerializer
from .models import User,DocumentDetails,BankDetails,Organization,OrganizationRole,OrganizationPermission


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"detail": "User registered successfully.", "token": str(token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "username": user.username})


class AuthenticatedUserView(APIView):
    @authenticate_view
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({"detail": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @authenticate_view
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT
            )
        except (AttributeError, Token.DoesNotExist):
            return Response({"detail": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

class UserView(BaseApiMixin, ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'email', 'aadhar_number', 'pan_number', 'role']
    pagination_class = StandardResultsPagination

    @authenticate_view
    @check_permissions
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user)
            return self.successful_get_response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UserSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return self.get_paginated_response([])
        
    @authenticate_view
    @check_permissions
    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

class DocumentDetailsViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view
    @check_permissions
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single DocumentDetails instance by its ID.
        """
        document = get_object_or_404(DocumentDetails, pk=kwargs.get("pk"))
        serializer = DocumentDetailsSerializer(document)
        return self.successful_get_response(serializer.data)

    @authenticate_view
    @check_permissions
    def post(self, request, *args, **kwargs):
        """
        Creates a new DocumentDetails instance from provided data.
        """
        serializer = DocumentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view
    @check_permissions
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing DocumentDetails instance.
        """
        document = get_object_or_404(DocumentDetailsSerializer, pk=kwargs.get("pk"))
        serializer = DocumentDetailsSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)
    
class BankDetailsViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view
    @check_permissions
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single BankDetails instance by its ID.
        """
        bank = get_object_or_404(BankDetails, pk=kwargs.get("pk"))
        serializer = BankDetailsSerializer(bank)
        return self.successful_get_response(serializer.data)

    @authenticate_view
    @check_permissions
    def post(self, request, *args, **kwargs):
        """
        Creates a new BankDetails instance from provided data.
        """
        serializer = BankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view
    @check_permissions
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing BankDetails instance.
        """
        bank = get_object_or_404(BankDetailsSerializer, pk=kwargs.get("pk"))
        serializer = BankDetailsSerializer(bank, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

class OrganizationViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view
    @check_permissions
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single Organization instance by its ID.
        """
        organization = get_object_or_404(Organization, pk=kwargs.get("pk"))
        serializer = OrganizationSerializer(organization)
        return self.successful_get_response(serializer.data)

    @authenticate_view
    def post(self, request, *args, **kwargs):
        """
        Creates a new Organization instance from provided data.
        """
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view
    @check_permissions
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing Organization instance.
        """
        organization = get_object_or_404(OrganizationSerializer, pk=kwargs.get("pk"))
        serializer = OrganizationSerializer(organization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

class OrganizationRoleViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view
    @check_permissions
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single OrganizationRole instance by its ID.
        """
        role = get_object_or_404(OrganizationRole, pk=kwargs.get("pk"))
        serializer = OrganizationRoleSerializer(role)
        return self.successful_get_response(serializer.data)

    @authenticate_view
    @check_permissions
    def post(self, request, *args, **kwargs):
        """
        Creates a new OrganizationRole instance from provided data.
        """
        serializer = OrganizationRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view
    @check_permissions
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing OrganizationRole instance.
        """
        role = get_object_or_404(OrganizationRoleSerializer, pk=kwargs.get("pk"))
        serializer = OrganizationRoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

class OrganizationPermissionViewSet(BaseApiMixin, ListAPIView):
    @authenticate_view
    @check_permissions
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single OrganizationPermission instance by its ID.
        """
        permission = get_object_or_404(OrganizationPermission, pk=kwargs.get("pk"))
        serializer = OrganizationPermissionSerializer(permission)
        return self.successful_get_response(serializer.data)

    @authenticate_view
    @check_permissions
    def post(self, request, *args, **kwargs):
        """
        Creates a new OrganizationPermission instance from provided data.
        """
        serializer = OrganizationPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)

    @authenticate_view
    @check_permissions
    def patch(self, request, *args, **kwargs):
        """
        Partially updates an existing OrganizationPermission instance.
        """
        permission = get_object_or_404(OrganizationPermissionSerializer, pk=kwargs.get("pk"))
        serializer = OrganizationPermissionSerializer(permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)