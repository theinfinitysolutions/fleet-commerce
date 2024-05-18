from threading import local

_thread_locals = local()


class ThreadLocalMiddleware(object):
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
    """returns the request object for this thread"""
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """returns the current user, if exist, otherwise returns None"""
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


def get_current_organisation():
    """returns the current user, if exist, otherwise returns None"""
    request = get_current_request()
    if request:
        return getattr(request, "organisation", None)
