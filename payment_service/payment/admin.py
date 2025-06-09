from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_order', 'amount', 'methodPayment',
                    'statusPayment', 'created_at')
    list_filter = ('statusPayment', 'methodPayment')
    search_fields = ('id_order', 'transaction_id')
