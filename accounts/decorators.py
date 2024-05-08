from functools import wraps
from django.urls import resolve
from django.db.models import Q

from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .authentication import BearerTokenAuthentication
from .models import OrganizationPermission
from .serializers import OrganizationRoleSerializer


def authenticate_view(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # Access the underlying HttpRequest if necessary
        _request = getattr(request, "_request", request)

        auth = get_authorization_header(_request).split()

        if not auth or auth[0].lower() != b"bearer":
            return JsonResponse(
                {"detail": "Authentication credentials were not provided or are incorrect."},
                status=401,
            )

        try:
            auth_token = auth[1].decode("utf-8")  # Ensure to decode from bytes to string
            authenticator = BearerTokenAuthentication()
            user, token = authenticator.authenticate_credentials(auth_token)
            _request.user = user  # Set the user in the original Django HttpRequest
        except AuthenticationFailed:
            return JsonResponse({"detail": "Invalid token."}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper

def check_permissions(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        role = OrganizationRoleSerializer(request.user.role)
        app_name = self.__module__.split(".")[0]
        method = request.method
        req_permission = f"{app_name}_{method}"
        permission = OrganizationPermission.objects.filter(
            Q(role=request.user.role) & Q(permission=req_permission)
        ).first()
        if not permission and role.data["role"] != "ADMIN":
            return JsonResponse(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )
        return func(self, request, *args, **kwargs)

    return wrapper