"""
Pagination module.
"""
from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """A paginator that divides data into pages."""

    page_size = 6
    page_size_query_param = 'page_size'
