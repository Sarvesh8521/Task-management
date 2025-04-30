
from django.db import models
from django.conf import settings
from .task import Task
from .project import Project

class TaskComment(models.Model):
    task = models.IntegerField()  
    project = models.IntegerField()  
    user = models.IntegerField()  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"