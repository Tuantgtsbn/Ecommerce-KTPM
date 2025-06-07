
from rest_framework import viewsets, status, filters
from .models import Clothes
from .serializers import ClothesSerializer
from rest_framework.decorators import action
from bson import ObjectId  # Import ObjectId từ thư viện bson
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
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
        if not ObjectId.is_valid(obj_id):  # Kiểm tra xem id có phải là ObjectId hợp lệ không
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
        action = request.data.get('action')
        if rating is None:
            return Response({'error': 'rating is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            rating = float(rating)
            if not (0 <= rating <= 5):
                raise ValueError
        except ValueError:
            return Response({'error': 'rating must be a number between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Nếu sản phẩm chưa có đánh giá, khởi tạo
        if action == 'new_comment':
            if cloth.rate is None or cloth.rate_count is None:
                cloth.rate = rating
                cloth.rate_count = 1
            else:
                cloth.rate = round((cloth.rate * cloth.rate_count + rating) / (cloth.rate_count+1), 2)
                cloth.rate_count += 1
                print(f"rate: {cloth.rate}, rate_count: {cloth.rate_count}")
        cloth.save()
        return Response({'message': 'Rating submitted successfully', 'average_rating': cloth.rate}, status=status.HTTP_200_OK)