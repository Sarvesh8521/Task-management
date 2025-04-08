
from django.db import models
from django.conf import settings
from .task import Task
from .project import Project
from .task_comment import TaskComment
from django.utils import timezone

class Notification(models.Model):
    NOTIFICATION_TYPES = [
    ('TASK_ASSIGNED', 'TASK_ASSIGNED'),
    ('PROJECT_ASSIGNED', 'PROJECT_ASSIGNED'),
    ('ORG_UPDATE', 'ORG_UPDATE'),
    ('TASK_COMMENT', 'TASK_COMMENT'),
   ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notify')  
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='notify')  
    work= models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='notify')  
    work_comment = models.ForeignKey(TaskComment, on_delete=models.CASCADE, null=True, blank=True,related_name='notify')  
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(timezone.now, editable=True)
    allow_notifications = models.BooleanField(default=True)  

    
    def organization(self):
        
        return self.project.organization if self.project else None

    def __str__(self):
        return f"Notify for {self.user.username}: {self.notification_type}"