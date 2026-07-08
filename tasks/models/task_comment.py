from django.db import models


class TaskComment(models.Model):
    task = models.IntegerField()
    project = models.IntegerField()
    user = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['project']),
        ]

    def __str__(self):
        return f"Comment by user {self.user} on task {self.task}"