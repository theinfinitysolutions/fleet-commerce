from functools import wraps

from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .authentication import BearerTokenAuthentication


def authenticate_view(role=None):
    def decorator(func):
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
                _request.organisation = user.organisation
                if role and not user.has_role(role):
                    return JsonResponse(
                        {"detail": "You do not have permission to perform this action."}, status=403
                    )

            except AuthenticationFailed:
                return JsonResponse({"detail": "Invalid token."}, status=401)

            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator
