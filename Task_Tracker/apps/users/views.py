from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    ViewSet для управления пользователями.

    Возможности:
    - Просмотр списка пользователей
    - Просмотр профиля пользователя
    - Создание пользователя
    - Обновление данных
    - Удаление пользователя

    Доступ:
    - Только авторизованные пользователи
    - Пользователь может видеть только себя (если нужно ограничение)
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return User.objects.none()
        
        if user.is_staff:
            return User.objects.all()

        return User.objects.filter(id=user.id)