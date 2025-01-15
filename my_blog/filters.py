from django_filters import rest_framework as filters
from .models import Product, Blog


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()  # Allows filtering by a price range
    name = filters.CharFilter(
        lookup_expr="icontains"
    )  # Case-insensitive search for product name
    category = filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )  # Category name filter

    class Meta:
        model = Product
        fields = ["price", "name", "category"]


class BlogFilter(filters.FilterSet):
    views = filters.RangeFilter()  # Allows filtering by views range
    title = filters.CharFilter(
        lookup_expr="icontains"
    )  # Case-insensitive search by title
    categories = filters.CharFilter(
        field_name="categories__name", lookup_expr="icontains"
    )  # Case-insensitive filter by category name

    class Meta:
        model = Blog
        fields = ["views", "title", "categories"]
