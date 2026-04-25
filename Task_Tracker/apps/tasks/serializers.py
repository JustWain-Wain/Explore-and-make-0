from rest_framework import serializers
from .models import Task, Comment
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Task.

    Преобразует объект задачи в JSON и обратно.
    Используется в API для создания и получения задач.
    """

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'status',
            'priority',
            'deadline',
            'created_at',
            'changed_at',
            'project',
            'author',
            'assignee',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'changed_at']
    

    def validate_name(self, name):
        "Проверка длины заголовка"

        if len(name.strip()) < 3:
            raise serializers.ValidationError(
                "Заголовок слишком короткий"
            )
        return name

    def validate_deadline(self, deadline):
        "Проверка даты окончания задачи"
        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError(
                "Дедлайн не может быть в прошлом"
            )
        return deadline
    

    def validate(self, data):
        "Проверка, является ли пользователь членом проекта"

        project = data.get('project')
        assignee = data.get('assignee')

        if project and assignee:
            if assignee not in project.members.all():
                raise serializers.ValidationError(
                    f"Пользователь {assignee} не состоит в проекте"
                )

        return data


    def create(self, validated_data):
        "Автор - пользователь, создавший задачу"

        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Преобразует объект комментария в JSON и обратно.
    Используется в API для создания и получения комментариев.
    """

    class Meta:
        model = Comment
        fields = [
            'id',
            'task',
            'author',
            'text',
            'created_at',
            'changed_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'changed_at']


    def validate_text(self, text):
        "Проверка длины комментария"

        if not text.strip():
            raise serializers.ValidationError(
                "Комментарий не может быть пустым"
            )
        return text


    def validate(self, data):
        "Проверка, является ли пользователь членом проекта"

        task = data.get('task')
        user = self.context['request'].user

        if task and user not in task.project.members.all():
            raise serializers.ValidationError(
                "Вы не участник проекта этой задачи"
            )

        return data


    def create(self, validated_data):
        "Автор - пользователь, оставивший комментарий"
        
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
