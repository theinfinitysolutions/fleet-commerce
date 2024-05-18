from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from accounts.filters import UserFilter
from fleet_commerce.mixin import BaseApiMixin
from pagination import StandardResultsPagination

from .decorators import authenticate_view
from .models import BankDetails, DocumentDetails, Organisation, Role, User
from .serializers import (
    BankDetailsSerializer,
    DocumentDetailsSerializer,
    OrganisationSerializer,
    UserSerializer,
)


class RegisterView(BaseApiMixin, ListAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return self.successful_post_response(
                {"detail": "User registered successfully.", "token": str(token)}
            )

        return self.error_response(errors=serializer.errors)


class CustomAuthToken(BaseApiMixin, ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return self.successful_post_response(
            {"token": token.key, "user_id": user.pk, "username": user.username}
        )


class AuthenticatedUserView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def get(self, request, *args, **kwargs):
        # add admin check for pk filter
        if "pk" in kwargs:
            user_detail = get_object_or_404(User, pk=kwargs.get("pk"))
        else:
            user_detail = request.user
        serializer = UserSerializer(user_detail)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        if "pk" in kwargs:
            user_detail = get_object_or_404(User, pk=kwargs.get("pk"))
        else:
            user_detail = request.user
        serializer = UserSerializer(user_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class UserListView(BaseApiMixin, ListAPIView):
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilter
    search_fields = ["name", "email", "aadhar_number", "pan_number", "role"]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        user = self.request.user
        if user.has_role(Role.SUPER_ADMIN):
            return User.objects.all()
        elif user.has_role(Role.ORGANISATION_ADMIN):
            return User.objects.filter(organisation=user.organisation)
        else:
            return User.objects.none()

    @authenticate_view(Role.ORGANISATION_ADMIN)
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return self.get_paginated_response([])


class LogoutView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return self.successful_post_response(
                {"detail": "Successfully logged out."}, status_code=status.HTTP_204_NO_CONTENT
            )
        except (AttributeError, Token.DoesNotExist):
            return self.error_response(errors={"detail": "Invalid request."})


class BankDetailsView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def post(self, request, *args, **kwargs):
        serializer = BankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)

        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def get(self, request, *args, **kwargs):
        bank_details = BankDetails.objects.filter(user=request.user)
        serializer = BankDetailsSerializer(bank_details, many=True)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        bank_details = get_object_or_404(BankDetails, pk=kwargs.get("pk"))
        serializer = BankDetailsSerializer(bank_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class DocumentDetailsView(BaseApiMixin, ListAPIView):
    @authenticate_view()
    def post(self, request, *args, **kwargs):
        serializer = DocumentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)

        return self.error_response(errors=serializer.errors)

    @authenticate_view()
    def get(self, request, *args, **kwargs):
        document_details = DocumentDetails.objects.filter(user=request.user)
        serializer = DocumentDetailsSerializer(document_details, many=True)
        return self.successful_get_response(serializer.data)

    @authenticate_view()
    def patch(self, request, *args, **kwargs):
        bank_details = get_object_or_404(DocumentDetails, pk=kwargs.get("pk"))
        serializer = DocumentDetailsSerializer(bank_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class OrganisationView(BaseApiMixin, ListAPIView):
    @authenticate_view(Role.SUPER_ADMIN)
    def post(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)

        return self.error_response(errors=serializer.errors)

    @authenticate_view(Role.SUPER_ADMIN)
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            organisation = get_object_or_404(Organisation, pk=kwargs.get("pk"))
            serializer = OrganisationSerializer(organisation)
            return self.successful_get_response(serializer.data)
        organisations = Organisation.objects.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return self.successful_get_response(serializer.data)

    @authenticate_view(Role.SUPER_ADMIN)
    def patch(self, request, *args, **kwargs):
        organisation = get_object_or_404(Organisation, pk=kwargs.get("pk"))
        serializer = OrganisationSerializer(organisation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)


class AssignRoleView(BaseApiMixin, ListAPIView):
    @authenticate_view(Role.ORGANISATION_ADMIN)
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data["user_id"])
        user.assign_role(request.data["role"])

        return self.successful_response("Role assigned.")


class RevokeRoleView(BaseApiMixin, ListAPIView):
    @authenticate_view(Role.ORGANISATION_ADMIN)
    def post(self, request):
        user = get_object_or_404(User, id=request.data["user_id"])
        user.revoke_role(request.data["role"])

        return self.successful_response("Role revoked successfully.")
