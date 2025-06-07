# comment/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Comment
import requests
from .serializers import CommentSerializer
from django.conf import settings
from bson import ObjectId
from ClassifyCommentModel.functions.classsify import classify
from ModelV3.test.test import classify_sentiment
from rest_framework.exceptions import NotFound
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_object(self):
        # Lấy id từ URL
        obj_id = self.kwargs.get('pk')
        if not ObjectId.is_valid(obj_id):  # Kiểm tra xem id có phải là ObjectId hợp lệ không
            raise NotFound({'error': 'Invalid ID format'})
        try:
            # Truy vấn đối tượng bằng ObjectId
            return Comment.objects.get(_id=ObjectId(obj_id))
        except Comment.DoesNotExist:
            raise NotFound({'error': 'Comment not found'})
    def perform_create(self, serializer):
        """
        Khi tạo comment, nếu rate không được gửi, tính tự động qua mô hình AI.
        """
        typeModel = self.request.data.get('typeModel', 'v1')
        comment_text = self.request.data.get('comment', '')
        rate_by_user = float(self.request.data.get('rateByUser', 0))
        
        if typeModel == 'v1':
            classify_ai = int(classify([comment_text])[0])
            sentimentType = "negative" if classify_ai == -1 else "positive"
            rate_by_ai = 0 if classify_ai == -1 else 5
        else:
            sentimentType = classify_sentiment(comment_text)
            if sentimentType == 'negative':
                rate_by_ai = 0
            elif sentimentType == 'positive':
                rate_by_ai = 5
            elif sentimentType == 'neutral':
                rate_by_ai = 3
        print('Rate by AI:', rate_by_ai)
        rate_avg = round((rate_by_ai+ rate_by_user)/2,2)
        comment_instance = serializer.save(rateByAi = rate_by_ai, rateAvg = rate_avg, sentimentType = sentimentType)
        # Gửi request tới product_service để cập nhật số lượng comment
        product_id = comment_instance.product_id
        category = comment_instance.category
        update_url = settings.ITEM_SERVICE_UPDATE_RATING_URL.format(category=category, product_id=product_id)
        payload = {
            "new_rate": rate_avg,
            "action": "new_comment"
        }
        try : 
            response = requests.post(update_url, json=payload)
            if response.status_code != 200:
                raise Exception(f"Update rating failed: {response.text}")
        except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='top/(?P<category>[^/.]+)')
    def top_products(self, request, category=None):
        """
        Lấy top 10 sản phẩm có mức độ hài lòng cao nhất theo category.
        Ta nhóm các bình luận theo product_id, tính trung bình rate, sắp xếp giảm dần.
        """
        if not category:
            return Response({'error': 'Category is required'}, status=status.HTTP_400_BAD_REQUEST)

        top_products = (Comment.objects.filter(category=category)
                        .values('product_id')
                        .annotate(avg_rate=Avg('rateAvg'), count=Count('product_id'))
                        .order_by('-avg_rate')[:10])

        if not top_products:
            return Response({'message': 'No products found for this category'}, status=status.HTTP_404_NOT_FOUND)

        formatted_products = [
            {
                'product_id': product['product_id'],
                'average_rating': product['avg_rate'],
                'comment_count': product['count']
            }
            for product in top_products
        ]
        return Response(formatted_products, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='analyze-comment')
    def analyze_comment(self, request) : 
        arrcomment = request.data.get('comments', [])
        print('Arrcomment:', arrcomment)
        if not arrcomment: 
            return Response({'error': 'Comments is required'}, status=status.HTTP_400_BAD_REQUEST)
        arrcommenttext = [comment.get('comment', '') for comment in arrcomment]
        print('Arrcommenttext:', arrcommenttext)
        result = classify(arrcommenttext)
        print('Result:', result)
        for i, comment in enumerate(arrcomment):
            comment['sentimentType'] = 'negative' if result[i] == -1 else 'positive'
        return Response(arrcomment, status=status.HTTP_200_OK)
@api_view(['GET'])
def list_comment(request):
    filters = {}
    if 'category' in request.query_params:
        filters['category'] = request.query_params['category']
    if 'product_id' in request.query_params:
        filters['product_id'] = request.query_params['product_id']
    if 'limit' in request.query_params:
        limit = int(request.query_params['limit'])
    if 'sentimentType' in request.query_params:
        filters['sentimentType'] = request.query_params['sentimentType']
    order_by = request.query_params.get('order_by', '-created_at')
    comments = Comment.objects.filter(**filters).order_by('-created_at')[:limit]
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)