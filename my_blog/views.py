from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import Product, Blog
from .serializers import ProductSerializer, BlogSerializer
from .filters import ProductFilter, BlogFilter
from .serializers import BlogSerializer
from .pagination import BlogPagination
from .permissions import IsAdminOrReadOnly
from .authentication import CustomTokenAuthentication


class UserDetailView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        user = request.user
        return Response(
            {
                "username": user.username,
                "email": user.email,
            }
        )


class BlogListView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = Blog.objects.all().order_by("-date_created")
        filterset = BlogFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        queryset = filterset.qs
        paginator = PageNumberPagination()
        paginator.page_size = 2  # Items per page
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BlogSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BlogDetailView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return None

    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BlogSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BlogSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
            )
        item.delete()
        return Response(
            {"message": "Blog with that id deleted!"}, status=status.HTTP_204_NO_CONTENT
        )


# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ProductFilter


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # No button is made since we are also creating
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "description", "category__name"]
    filterset_class = ProductFilter

    def delete(self, request, *args, **kwargs):
        Product.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    filter_backends = [SearchFilter]
    search_fields = ["name", "description", "category__name"]
