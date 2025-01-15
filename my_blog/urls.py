from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    BlogListView,
    ProductListCreateView,
    ProductRetrieveUpdateDestoryView,
    UserDetailView,
    BlogDetailView,
)

urlpatterns = [
    path("blogs/", BlogListView.as_view(), name="blog-list"),
    path("blogs/<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
    path("products/", ProductListCreateView.as_view(), name="product-list"),
    path(
        "products/<int:pk>/",
        ProductRetrieveUpdateDestoryView.as_view(),
        name="product-detail",
    ),
    path("user/", UserDetailView.as_view(), name="user_detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
