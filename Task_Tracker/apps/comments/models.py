from django.db import models

class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
