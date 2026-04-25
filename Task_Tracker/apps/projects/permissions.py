from rest_framework.permissions import BasePermission
from .models import ProjectMember
from .utils import is_owner


class ProjectPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
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