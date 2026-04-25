from django.utils import timezone
from rest_framework import serializers
from .models import Project, ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
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
        project = self.context['project']
        user = attrs['user']

        if ProjectMember.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError('Пользователь уже состоит в проекте.')
        return attrs

    def create(self, validated_data):
        validated_data.setdefault('role', 'member')
        return ProjectMember.objects.create(
            project=self.context['project'],
            **validated_data,
        )


class ProjectSerializer(serializers.ModelSerializer):
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
        if len(name.strip()) < 3:
            raise serializers.ValidationError('Заголовок слишком короткий.')
        return name

    def validate_deadline(self, deadline):
        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError('Дедлайн не может быть в прошлом.')
        return deadline

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(creator=user, **validated_data)
        ProjectMember.objects.create(project=project, user=user, role='owner')
        return project
