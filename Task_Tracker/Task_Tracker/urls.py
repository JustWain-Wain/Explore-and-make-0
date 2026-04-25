from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from apps.projects.views import ProjectViewSet
from apps.tasks.views import TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tasks', TaskViewSet, basename='tasks')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', get_schema_view(title='Task Tracker API'), name='api-schema'),
    path(
        'api/docs/swagger/',
        TemplateView.as_view(template_name='swagger.html'),
        name='swagger-ui',
    ),
    path(
        'api/docs/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc-ui',
    ),
]
