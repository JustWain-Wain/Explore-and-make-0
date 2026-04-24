from django.db import models

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
        default='new'
    )
    priority = models.CharField(
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    deadline = models.DateTimeField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey('projects.Project', related_name='tasks', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)
    assignees = models.ManyToManyField('auth.User', related_name='assigned_tasks')

    comments = models.ManyToManyField('Comment', related_name='tasks')
