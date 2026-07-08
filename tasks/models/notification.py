from django.db import models
from django.conf import settings
from django.utils import timezone
from .task import Task
from .project import Project
from .task_comment import TaskComment


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('TASK_ASSIGNED', 'Task Assigned'),
        ('PROJECT_ASSIGNED', 'Project Assigned'),
        ('ORG_UPDATE', 'Organization Update'),
        ('TASK_COMMENT', 'Task Comment'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    work = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    work_comment = models.ForeignKey(TaskComment, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    allow_notifications = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def organization(self):
        return self.project.organization if self.project else None

    def __str__(self):
        return f"Notification for {self.user}: {self.notification_type}"