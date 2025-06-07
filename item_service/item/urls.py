# item_service/urls.py
from django.urls import path
from .views import search_item  # cùng với các view khác nếu có
from .views import update_rating
urlpatterns = [
    path('api/items/search/<str:item_type>/', search_item, name='search-item'),
    path('api/items/<str:category>/<str:product_id>/update_rating/', update_rating, name='update-rating'),
    # Các endpoint khác ví dụ:
    # path('api/items/cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    # path('api/items/cart/', ViewCartView.as_view(), name='view-cart'),
]
