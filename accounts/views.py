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
from .decorators import authenticate_view
from .serializers import UserSerializer
from .models import User


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
    search_fields = ['name', 'email', 'aadhar_number', 'pan_number']
    pagination_class = StandardResultsPagination

    @authenticate_view
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
    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.successful_post_response(serializer.data)
        return self.error_response(errors=serializer.errors)