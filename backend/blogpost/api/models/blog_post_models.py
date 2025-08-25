# api/models.py
from django.db import models
from ..models.user_models import UserInfo

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Stored in folder
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
