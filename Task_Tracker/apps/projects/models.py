from django.db import models
from django.conf import settings

class Project(models.Model):
    """
    Модель проекта.

    Хранит информацию о проекте:
    название, описание,
    создатель проекта, участники,
    дату создания, изменения, окончания проекта.
    """

    name = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects',
        null=True,
        blank=True
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMember',
        related_name='projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Возвращает название проекта."""
        return self.name


class ProjectMember(models.Model):
    """
    Модель участника проекта.

    Хранит информацию об участниках проекта и их ролях.

    Используется для отделения владельца проекта от участников.
    """

    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('member', 'Member'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        """
        Возвращает строковое представление
        пользователя в проекте и его роль.
        """
        return f'{self.user} - {self.project} ({self.role})'
