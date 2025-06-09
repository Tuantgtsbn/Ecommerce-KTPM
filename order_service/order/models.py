from django.db import models
from django.utils import timezone
# Create your models here.


class Order (models.Model):
    orderStatus = models.CharField(max_length=255, default='pending')
    amount = models.FloatField(default=0)
    address = models.TextField(blank=False, null=False)
    id_customer = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    methodPayment = models.CharField(max_length=255, default='cash')
    statusPayment = models.CharField(max_length=255, default='pending')

    def __str__(self):
        return f"Order #{self.id} của {self.id_customer}"

    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    id_item = models.CharField(max_length=255, blank=False, null=False)
    category = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"Item {self.id_item} trong Order #{self.order.id}"
