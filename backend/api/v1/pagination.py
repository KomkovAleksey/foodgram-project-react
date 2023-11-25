"""
Pagination module.
"""
from rest_framework import pagination

from core.constants import MAX_PAGE_SIZE


class CustomPagination(pagination.PageNumberPagination):
    """A paginator that divides data into pages."""

    page_size_query_param = 'limit'
    page_size = MAX_PAGE_SIZE
