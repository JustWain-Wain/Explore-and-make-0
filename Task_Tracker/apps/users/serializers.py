from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.

    Преобразует объект пользователя в JSON и обратно.
    Используется в API для создания и получения пользователей.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'middle_name',
            'position',
        ]


    def create(self, validated_data):
        "Пароль не должен записываться в бд"
        
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
