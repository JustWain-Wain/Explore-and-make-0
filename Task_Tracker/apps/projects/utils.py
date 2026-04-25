from .models import ProjectMember

def is_owner(user, project):
        """Проверяет является ли пользователь владельцем проекта."""
        return ProjectMember.objects.filter(
            user=user,
            project=project,
            role='owner'
        ).exists()
