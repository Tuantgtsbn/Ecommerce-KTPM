from django.db import models
from django.utils import timezone

# Create your models here.


class Payment(models.Model):
    id_order = models.CharField(max_length=50)
    amount = models.FloatField(default=0)
    methodPayment = models.CharField(max_length=255, default='cash')
    statusPayment = models.CharField(max_length=255, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment #{self.id} của Order #{self.id_order}"

    class Meta:
        db_table = 'payment'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        ordering = ['-created_at']
