from django.utils.dateparse import parse_date
from rest_framework.viewsets import ModelViewSet
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .permissions import TaskPermission, CommentPermission


class TaskViewSet(ModelViewSet):
    """
    ViewSet для управления задачами.

    CRUD:
    - list, retrieve, create, update, destroy

    Доступ:
    - Только для участников проекта задачи

    Фильтрация (query params):
    - project — по проекту
    - status — по статусу
    - priority — по приоритету
    - assignee — по исполнителю
    - deadline_from / deadline_to — по диапазону дедлайна
    """

    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(
            project__project_memberships__user=user
        ).select_related('project', 'author', 'assignee').distinct()

        project_id = self.request.query_params.get('project')
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        assignee_id = self.request.query_params.get('assignee')
        deadline_from = self.request.query_params.get('deadline_from')
        deadline_to = self.request.query_params.get('deadline_to')

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if assignee_id:
            queryset = queryset.filter(assignee_id=assignee_id)
        if deadline_from:
            parsed = parse_date(deadline_from)
            if parsed:
                queryset = queryset.filter(deadline__date__gte=parsed)
        if deadline_to:
            parsed = parse_date(deadline_to)
            if parsed:
                queryset = queryset.filter(deadline__date__lte=parsed)

        return queryset


class CommentViewSet(ModelViewSet):
    """
    ViewSet для управления комментариями.

    CRUD:
    - list, retrieve, create, update, destroy

    Доступ:
    - Только для участников проекта, к которому относится задача
    """
    
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(
            task__project__project_memberships__user=user
        ).select_related('task', 'author').distinct()
