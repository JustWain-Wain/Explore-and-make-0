from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    members = models.ManyToManyField('auth.User', related_name='projects')
    tasks = models.ManyToManyField('tasks.Task', related_name='projects')

    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=None)
