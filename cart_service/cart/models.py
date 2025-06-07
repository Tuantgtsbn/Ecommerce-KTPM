from django.db import models
from django.conf import settings

class Cart(models.Model):
    customer_id = models.CharField(max_length=255, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Cart #{self.id} của {self.customer.username}"

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    item_id = models.IntegerField()  # Lưu ID của sản phẩm từ service Item
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.item_id} x {self.quantity} trong Cart #{self.cart_id}"
