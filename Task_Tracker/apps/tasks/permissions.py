from rest_framework.permissions import BasePermission

class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user not in obj.project.members.all():
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if view.action == 'partial_update':
            if 'status' in request.data or 'priority' in request.data:
                return obj.assignee == user

        if view.action in ['update', 'partial_update']:
            return obj.author == user

        if view.action == 'destroy':
            return obj.author == user

        return False


class CommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user not in obj.task.project.members.all():
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        if view.action in ['update', 'destroy']:
            return obj.author == user

        return True