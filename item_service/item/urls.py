# item_service/urls.py
from django.urls import path
from .views import get_item_detail, search_items, update_rating

urlpatterns = [
    # Giữ lại các URL hiện có
    path('api/items/<str:category>/search/',
         search_items, name='search-items'),
    path('api/items/<str:category>/<str:product_id>/update_rating/',
         update_rating, name='update-rating'),

    # Thêm URL mới
    path('api/items/<str:category>/<str:item_id>/',
         get_item_detail, name='get-item-detail'),

]
