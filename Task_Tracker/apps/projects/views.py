from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Project, ProjectMember
from .permissions import ProjectPermission
from .serializers import ProjectSerializer, ProjectMemberSerializer
from .utils import is_owner


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(project_memberships__user=user).distinct()

    @action(detail=True, methods=['get', 'post'], url_path='members')
    def members(self, request, pk=None):
        project = self.get_object()

        if request.method == 'GET':
            queryset = project.project_memberships.select_related('user').all()
            serializer = ProjectMemberSerializer(queryset, many=True)
            return Response(serializer.data)

        if not is_owner(request.user, project):
            return Response(
                {'detail': 'Только владелец проекта может добавлять участников.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProjectMemberSerializer(
            data=request.data,
            context={'project': project},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path=r'members/(?P<user_id>\d+)')
    def remove_member(self, request, pk=None, user_id=None):
        project = self.get_object()

        if not is_owner(request.user, project):
            return Response(
                {'detail': 'Только владелец проекта может удалять участников.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        membership = ProjectMember.objects.filter(project=project, user_id=user_id).first()
        if membership is None:
            return Response(
                {'detail': 'Участник не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if membership.role == 'owner':
            return Response(
                {'detail': 'Нельзя удалить владельца проекта из участников.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
