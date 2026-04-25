from django.utils import timezone
from rest_framework import serializers
from .models import Project, ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ProjectMember.

    Преобразует объект участника проекта в JSON и обратно.
    Используется в API для создания и получения участников проекта.
    """

    class Meta:
        model = ProjectMember
        fields = [
            'id',
            'project',
            'user',
            'role'
        ]
        read_only_fields = ['id', 'project']
        extra_kwargs = {'role': {'required': False}}

    def validate(self, attrs):
        """
        Выполняет валидацию входных данных перед созданием участника проекта.

        Проверяет, что пользователь ещё не добавлен в указанный проект.
        Проект берётся из контекста сериализатора (self.context['project']).
        """
        project = self.context['project']
        user = attrs['user']

        if ProjectMember.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError('Пользователь уже состоит в проекте.')
        return attrs

    def create(self, validated_data):
        """
        Создаёт нового участника проекта.

        Автоматически:
        - подставляет проект из контекста сериализатора (self.context['project'])
        - устанавливает роль 'member' по умолчанию, если она не передана
        """
        validated_data.setdefault('role', 'member')
        return ProjectMember.objects.create(
            project=self.context['project'],
            **validated_data,
        )


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Project.

    Преобразует объект проекта в JSON и обратно.
    Используется в API для создания и получения проектов.
    """

    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'creator',
            'created_at',
            'changed_at',
            'deadline',
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'changed_at']

    def validate_name(self, name):
        """Проверяет, что длина заголовка больше либо равна 3."""
        if len(name.strip()) < 3:
            raise serializers.ValidationError('Заголовок слишком короткий.')
        return name

    def validate_deadline(self, deadline):
        """Проверяет, что дедлайн не находится в прошлом."""
        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError('Дедлайн не может быть в прошлом.')
        return deadline

    def create(self, validated_data):
        """
        Создает новый проект.

        Автоматически устанавливает роль 'owner' создателю проекта
        """
        user = self.context['request'].user
        project = Project.objects.create(creator=user, **validated_data)
        ProjectMember.objects.create(project=project, user=user, role='owner')
        return project
