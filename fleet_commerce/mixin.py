from rest_framework import status
from rest_framework.response import Response

CONTENT_TYPE_JSON = "application/json; charset=utf-8"


class BaseApiMixin(object):
    def error_response(self, message="", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {"response": message, "errors": errors},
            status=status_code,
            content_type=CONTENT_TYPE_JSON,
        )

    def forbidden_response(
        self, message="Access denied", errors=None, status_code=status.HTTP_403_FORBIDDEN
    ):
        return Response(
            {"message": message, "errors": errors},
            status=status_code,
            content_type=CONTENT_TYPE_JSON,
        )

    def successful_post_response(self, message="", status_code=status.HTTP_201_CREATED):
        return Response(message, status=status_code, content_type=CONTENT_TYPE_JSON)

    def successful_response(self, message="", status_code=status.HTTP_200_OK):
        return Response({"message": message}, status=status_code, content_type=CONTENT_TYPE_JSON)

    def not_found_response(self, message="Not found", status_code=status.HTTP_404_NOT_FOUND):
        return Response({"message": message}, status=status_code, content_type=CONTENT_TYPE_JSON)

    def successful_get_response(self, message="", status_code=status.HTTP_200_OK):
        return Response(message, status=status_code, content_type=CONTENT_TYPE_JSON)
