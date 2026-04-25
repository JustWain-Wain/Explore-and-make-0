from rest_framework import serializers
from .models import Project
from django.utils import timezone

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'members',
            'created_at',
            'changed_at',
            'deadline'
        ]
        read_only_fields = ['id', 'created_at', 'changed_at']


    def validate_name(self, name):
        "Проверка длины заголовка"
        
        if len(name.strip()) < 3:
            raise serializers.ValidationError(
                "Заголовок слишком короткий"
            )
        return name


    def validate_deadline(self, deadline):
        "Проверка даты окончания проекта"

        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError(
                "Дедлайн не может быть в прошлом"
            )
        return deadline
