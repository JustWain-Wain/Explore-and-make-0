from rest_framework import serializers
from .models import Task
from datetime import datetime

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    
    def validate_deadline(self, deadline):
        if deadline <= datetime.now():
            raise serializers.ValidationError("Дедлайн не может быть в прошлом")
        return deadline

    def validate_creation_date(self, created_at):
        if created_at > datetime.now():
            raise serializers.ValidationError("Дата создания должна быть в настоящем или прошлом")
        return created_at