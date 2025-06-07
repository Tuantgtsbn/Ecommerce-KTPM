
from rest_framework import viewsets, filters, status
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import action
from bson import ObjectId  # Import ObjectId từ thư viện bson
from rest_framework.exceptions import NotFound
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'description', 'name']  # Tìm kiếm theo các trường này
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
            return Book.objects.get(_id=ObjectId(obj_id))
        except Book.DoesNotExist:
            raise NotFound({'error': 'Book not found'})
# Chức năng bổ sung 1: Áp dụng giảm giá
    @action(detail=True, methods=['post'])
    def discount(self, request, pk=None):
        book = self.get_object()
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
        original_price = book.price
        book.price = round(original_price * (1 - discount_percent/100),2)
        book.save()
        return Response({'message': 'Discount applied successfully', 'new_price': book.price}, status=status.HTTP_200_OK)

    # Chức năng bổ sung 2: Đánh giá sản phẩm
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        book = self.get_object()
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
            if book.rate is None or book.rate_count is None:
                book.rate = rating
                book.rate_count = 1
            else:
                book.rate = round((book.rate * book.rate_count + rating) / (book.rate_count+1),2)
                book.rate_count += 1
        book.save()
        return Response({'message': 'Rating submitted successfully', 'average_rating': book.rate}, status=status.HTTP_200_OK)