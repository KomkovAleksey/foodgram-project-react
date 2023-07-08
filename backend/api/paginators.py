"""
Pagination module.
"""
from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Пагинатор разделяющий данные на страницы с заданным лимитом."""
    page_size = 6
    page_size_query_param = 'limit'
