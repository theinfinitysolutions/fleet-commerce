from django.core.paginator import EmptyPage, Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 100
    start_after_id = "offset"  # New query parameter

    def paginate_queryset(self, queryset, request, view=None):
        """
        Optionally restricts the queryset by filtering against a `start_after` query parameter
        in the request.
        """
        start_after = request.query_params.get(self.start_after_id)
        if start_after is not None:
            queryset = queryset.filter(id__gt=start_after)

        return super().paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "results": data,
            }
        )
