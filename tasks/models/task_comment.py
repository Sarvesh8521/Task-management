
from django.db import models
from django.conf import settings
from .task import Task
from .project import Project

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')  
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task_comments')  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_comments')  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"