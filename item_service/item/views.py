# item_service/views.py
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer


@api_view(['GET'])
def get_item_detail(request, category, item_id):
    """
    Lấy chi tiết sản phẩm dựa vào id_item và category
    """
    try:
        # Xác định URL của service dựa trên category
        if category.lower() == 'book':
            service_url = f"{settings.BOOK_SERVICE_URL}{item_id}/"
        elif category.lower() == 'clothes':
            service_url = f"{settings.CLOTHES_SERVICE_URL}{item_id}/"
        else:
            return Response({'error': f'Category "{category}" is not supported.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Gọi API của service tương ứng
        response = requests.get(service_url)

        if response.status_code == 200:
            # Lưu thông tin item vào database nếu chưa tồn tại
            Item.objects.get_or_create(
                id_item=item_id,
                category=category.lower()
            )

            # Trả về dữ liệu từ service
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': f'Failed to retrieve data from {category} service. Status code: {response.status_code}'},
                status=response.status_code
            )

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def search_items(request, category):
    """
    Tìm kiếm sản phẩm theo category và từ khóa
    """
    query = request.GET.get('q', '')

    if not query:
        return Response({'error': 'Search query is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Xác định URL của service dựa trên category
        if category.lower() == 'book':
            service_url = f"{settings.BOOK_SERVICE_URL}search/"
        elif category.lower() == 'clothes':
            service_url = f"{settings.CLOTHES_SERVICE_URL}search/"
        else:
            return Response({'error': f'Category "{category}" is not supported.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Gọi API của service tương ứng
        response = requests.get(service_url, params={'q': query})

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': f'Failed to search data from {category} service. Status code: {response.status_code}'},
                status=response.status_code
            )

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

    if category.lower() == 'book':
        service_url = settings.BOOK_SERVICE_UPDATE_RATING_URL.format(
            product_id=product_id)
    elif category.lower() == 'clothes':
        service_url = settings.CLOTHES_SERVICE_UPDATE_RATING_URL.format(
            product_id=product_id)
    else:
        return Response({'error': f'Category "{category}" is not supported.'},
                        status=status.HTTP_400_BAD_REQUEST)

    payload = {
        "new_rate": new_rate
    }

    try:
        resp = requests.post(service_url, json=payload)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if resp.status_code != 200:
        return Response({'error': f'Failed to update rating: {resp.text}'},
                        status=resp.status_code)

    return Response(resp.json(), status=status.HTTP_200_OK)
