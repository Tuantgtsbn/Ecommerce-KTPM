# comment/models.py
from django.db import models

class Comment(models.Model):
    user_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    comment = models.TextField()
    sentimentType = models.CharField(max_length=50, default="positive")  # positive, negative
    rateByUser = models.FloatField(default=0)  
    rateByAi = models.FloatField(default=0)  # Giá trị đo mức độ hài lòng, sẽ được tính qua mô hình AI
    rateAvg = models.FloatField(default=0)  # Giá trị đo mức độ hài lòng trung bình
    category = models.CharField(max_length=50)  # Ví dụ: "book", "laptop", ...
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Comment by {self.user_id} on {self.product_id} in category {self.category}"
