from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    priority = models.CharField(max_length=20, default='medium')
    deadline = models.DateTimeField(default=None)
    project = models.ForeignKey('projects.Project', related_name='tasks', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)
    assignees = models.ManyToManyField('auth.User', related_name='assigned_tasks')
    comments = models.ManyToManyField('Comment', related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
