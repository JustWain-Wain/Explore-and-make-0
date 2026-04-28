from rest_framework.permissions import BasePermission

class TaskPermission(BasePermission):
    """
    Разрешает доступ только владельцу участникам проекта.

    Проверяет, что пользователь является участником проекта и исполнителем задачи.
    Используется для ограничения доступа к задачам.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяет, что пользователь участник проекта и исполнитель задачи."""
        user = request.user

        if user not in obj.project.members.all():
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if view.action == 'partial_update':
            if 'status' in request.data or 'priority' in request.data:
                return obj.assignee == user

        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.author == user

        return False


class CommentPermission(BasePermission):
    """
    Разрешает доступ только владельцу участникам проекта.

    Проверяет, что пользователь является участником проекта.
    Используется для ограничения доступа к удалению комментария.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяет, что пользователь является участником проекта."""
        user = request.user

        if user not in obj.task.project.members.all():
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        if view.action in ['update', 'destroy']:
            return obj.author == user

        return True