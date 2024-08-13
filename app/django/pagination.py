from rest_framework.pagination import PageNumberPagination

from app.constants import Pagination


class CustomPagination(PageNumberPagination):
    max_page_size = Pagination.MAX_PAGE_SIZE
    page_size_query_param = Pagination.PAGE_SIZE_QUERY_PARAM
