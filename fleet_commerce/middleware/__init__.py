from threading import local

from rest_framework.authentication import get_authorization_header

from accounts.authentication import BearerTokenAuthentication

_thread_locals = local()


class ThreadLocalMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        clear_thread_locals()
        return response

    def process_exception(self, request, exception):
        clear_thread_locals()


def clear_thread_locals():
    if hasattr(_thread_locals, "request"):
        del _thread_locals.request


def get_current_request():
    """Returns the request object for this thread."""
    _request = getattr(_thread_locals, "request", None)
    if _request:
        if not hasattr(_request, "user"):
            auth = get_authorization_header(_request).split()
            if len(auth) == 2 and auth[0].lower() == b"bearer":
                auth_token = auth[1].decode("utf-8")  # Ensure to decode from bytes to string
                authenticator = BearerTokenAuthentication()
                user, token = authenticator.authenticate_credentials(auth_token)
                _request.user = user  # Set the user in the original Django HttpRequest
                _request.organisation = user.organisation
        else:
            user = _request.user
        if not hasattr(_request, "organisation"):
            if user:
                _request.organisation = user.organisation

    return _request


def get_current_user():
    """Returns the current user, if exist, otherwise returns None."""
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


def get_current_organisation():
    """Returns the current organisation, if exist, otherwise returns None."""
    request = get_current_request()
    if request:
        return getattr(request, "organisation", None)
