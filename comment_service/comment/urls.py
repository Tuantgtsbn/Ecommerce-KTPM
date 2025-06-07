# book/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, list_comment
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('comments/list/', list_comment, name='list_comment'),
    path('', include(router.urls)),
]
