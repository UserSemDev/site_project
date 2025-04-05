from rest_framework.pagination import PageNumberPagination


class EventPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "items_count"
    max_page_size = 100
