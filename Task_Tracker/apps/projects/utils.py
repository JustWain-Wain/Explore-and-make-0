from .models import ProjectMember

def is_owner(user, project):
        return ProjectMember.objects.filter(
            user=user,
            project=project,
            role='owner'
        ).exists()
