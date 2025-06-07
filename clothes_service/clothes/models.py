
from djongo import models

class Clothes(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255, default='Unknown')
    title = models.CharField(max_length=255, default='')
    brand = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    thumbnail = models.URLField(blank=True, null=True)
    images = models.JSONField(blank=True, null=True)  # Lưu danh sách URL ảnh minh họa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rate = models.FloatField(default=0)
    rate_count = models.IntegerField(default=0)
    category = models.CharField(max_length=255, default='clothes')
    objects = models.DjongoManager()

    def __str__(self):
        return self.name
