from rest_framework import serializers
from .models import Comment
from datetime import datetime

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    
    def validate_creation_date(self, created_at):
        if created_at > datetime.now():
            raise serializers.ValidationError("Дата создания должна быть в настоящем или прошлом")
        return created_at