from django.db import models
from .project import Project


class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("in_review", "In Review"),
        ("completed", "Completed"),
        ("blocked", "Blocked"),
    ]

    ISSUE_TYPE_CHOICES = [
        ("epic", "Epic"),
        ("story", "Story"),
        ("task", "Task"),
        ("bug", "Bug"),
        ("subtask", "Sub-task"),
    ]

    PRIORITY_CHOICES = [
        ("highest", "Highest"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
        ("lowest", "Lowest"),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    project = models.IntegerField()
    users = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES, default="task")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sprint = models.CharField(max_length=100, null=True, blank=True, default="1")
    release_version = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-creation_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['project']),
            models.Index(fields=['users']),
            models.Index(fields=['priority']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name
