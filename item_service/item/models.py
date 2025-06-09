from django.db import models

# Create your models here.


class Item(models.Model):
    id_item = models.CharField(max_length=255, primary_key=True)
    category = models.CharField(max_length=100)  # book, clothes, etc.

    def __str__(self):
        return f"{self.category}: {self.id_item}"

    class Meta:
        unique_together = ('id_item', 'category')
