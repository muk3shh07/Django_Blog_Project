from rest_framework.pagination import PageNumberPagination


class BlogPagination(PageNumberPagination):
    page_size = 5  # Items per page
    page_size_query_param = "page_size"  # Allow clients to override
    max_page_size = 100  # Maximum items per page
