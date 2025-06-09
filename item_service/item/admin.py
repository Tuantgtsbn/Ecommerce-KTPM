from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'category')
    list_filter = ('category',)
    search_fields = ('id_item', 'category')
