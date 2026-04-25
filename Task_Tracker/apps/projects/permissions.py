from rest_framework.permissions import BasePermission
from .models import ProjectMember
from .utils import is_owner


class ProjectPermission(BasePermission):
    """
    Разрешает доступ только владельцу и участникам проекта.

    Проверяет, что пользователь является участником проекта.
    Используется для ограничения доступа к данным проекта.
    """

    def has_permission(self, request, view):
        """Проверяет, что пользователь существует и авторизован."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверяет, что пользователь участник проекта и предоставляет права."""
        user = request.user

        is_member = ProjectMember.objects.filter(
            user=user,
            project=obj
        ).exists()

        if not is_member:
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return is_owner(user, obj)
