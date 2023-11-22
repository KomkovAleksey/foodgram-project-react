"""
Pagination module.
"""
from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """A paginator that divides data into pages."""

    page_size_query_param = "limit"
    page_size = 6
