
from rest_framework import viewsets, status, filters
from .models import Clothes
from .serializers import ClothesSerializer
from rest_framework.decorators import action
from bson import ObjectId  # Import ObjectId từ thư viện bson
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from django.db import models


class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'brand', 'description', 'name']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })

    def get_object(self):
        # Lấy id từ URL
        obj_id = self.kwargs.get('pk')
        # Kiểm tra xem id có phải là ObjectId hợp lệ không
        if not ObjectId.is_valid(obj_id):
            raise NotFound({'error': 'Invalid ID format'})
        try:
            # Truy vấn đối tượng bằng ObjectId
            return Clothes.objects.get(_id=ObjectId(obj_id))
        except Clothes.DoesNotExist:
            raise NotFound({'error': 'Clothes not found'})
# Chức năng bổ sung 1: Áp dụng giảm giá

    @action(detail=True, methods=['post'])
    def discount(self, request, pk=None):
        cloth = self.get_object()
        discount_percent = request.data.get('discount_percent')
        if discount_percent is None:
            return Response({'error': 'discount_percent is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            discount_percent = float(discount_percent)
            if not (0 <= discount_percent <= 100):
                raise ValueError
        except ValueError:
            return Response({'error': 'discount_percent must be a number between 0 and 100'}, status=status.HTTP_400_BAD_REQUEST)

        # Tính giá mới
        original_price = cloth.price
        cloth.price = round(original_price * (1 - discount_percent / 100), 2)
        cloth.save()
        return Response({'message': 'Discount applied successfully', 'new_price': cloth.price}, status=status.HTTP_200_OK)

    # Chức năng bổ sung 2: Đánh giá sản phẩm
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        cloth = self.get_object()
        rating = request.data.get('new_rate')

        if rating is None:
            return Response({'error': 'rating is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = float(rating)
            if not (0 <= rating <= 5):
                raise ValueError
        except ValueError:
            return Response({'error': 'rating must be a number between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        # Cập nhật đánh giá cho sản phẩm
        if cloth.rate is None or cloth.rate_count is None:
            cloth.rate = rating
            cloth.rate_count = 1
        else:
            # Tính toán đánh giá trung bình mới
            cloth.rate = round((cloth.rate * cloth.rate_count +
                                rating) / (cloth.rate_count + 1), 2)
            cloth.rate_count += 1

        cloth.save()

        return Response({
            'message': 'Rating submitted successfully',
            'average_rating': cloth.rate,
            'rating_count': cloth.rate_count
        }, status=status.HTTP_200_OK)
    # Thêm action search

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Tìm kiếm sách theo từ khóa
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Search query is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Sử dụng filter để tìm kiếm
        queryset = self.get_queryset().filter(
            models.Q(title__icontains=query) |
            models.Q(brand__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(name__icontains=query)
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })
