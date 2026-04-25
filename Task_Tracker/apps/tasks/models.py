from django.db import models
from django.conf import settings

STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('review', 'На проверке'),
        ('done', 'Завершена'),
    ]

PRIORITY_CHOICES = [
    ('low', 'Низкий'),
    ('medium', 'Средний'),
    ('high', 'Высокий'),
    ('urgent', 'Срочно')
]

class Task(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='new',
        max_length=20
    )
    priority = models.CharField(
        choices=PRIORITY_CHOICES,
        default='medium',
        max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)

    project = models.ForeignKey(
        'projects.Project',
        related_name='tasks',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tasks',
        on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_tasks'
    )


class Comment(models.Model):
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
