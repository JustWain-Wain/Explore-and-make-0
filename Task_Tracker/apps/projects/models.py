from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects'
    )
    tasks = models.ManyToManyField(
        'tasks.Task',
        related_name='projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
