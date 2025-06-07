# item_service/views.py
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def search_item(request, item_type):
    """
    Tìm kiếm sản phẩm theo loại. Ví dụ: /api/items/search/book?q=keyword
    Tham số query 'q' dùng để tìm kiếm theo tên hoặc mô tả sản phẩm.
    """
    query = request.GET.get('q', '')
    results = []
    
    # Xác định URL của service dựa trên item_type
    if item_type.lower() == 'book':
        service_url = settings.BOOK_SERVICE_URL  # Ví dụ: 'http://localhost:8001/api/books/'
    elif item_type.lower() == 'clothes':
        service_url = settings.CLOTHES_SERVICE_URL  # Ví dụ: 'http://localhost:8002/api/laptops/'
    else:
        return Response({'error': f'Item type "{item_type}" is not supported.'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Gọi API của service tương ứng với tham số tìm kiếm
    try:
        response = requests.get(service_url, params={'search': query})
        if response.status_code == 200:
            
            results = response.json()
            
        else:
            return Response({'error': 'Failed to retrieve data from service.'},
                            status=response.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(results, status=status.HTTP_200_OK)

@api_view(['POST'])
def update_rating(request, category, product_id):
    """
    Cập nhật rating của sản phẩm sau khi có comment mới.
    """
    try:
        new_rate = float(request.data.get("new_rate"))
    except (TypeError, ValueError):
        return Response({"error": "new_rate must be provided and be a number."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    action = request.data.get("action")
    if not action:
        return Response({"error": "action is required."},
                        status=status.HTTP_400_BAD_REQUEST)
    if category.lower() == 'book':
        service_url = settings.BOOK_SERVICE_UPDATE_RATING_URL.format(product_id=product_id)
    elif category.lower() == 'clothes':
        service_url = settings.CLOTHES_SERVICE_UPDATE_RATING_URL.format(product_id=product_id)
    else :
        return Response({'error': f'Category "{category}" is not supported.'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    payload = {
        "new_rate": new_rate,
        "action": action
    }
    try:
        resp = requests.post(service_url, json=payload)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if resp.status_code != 200:
        return Response({'error': f'Failed to update rating: {resp.text}'},
                        status=resp.status_code)
    return Response({'message': 'Rating updated successfully'}, status=status.HTTP_200_OK)
