# book/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClothesViewSet

router = DefaultRouter()
router.register(r'clothes', ClothesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
