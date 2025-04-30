from django.db import models
from .project import Project
from django.conf import settings
    

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("in_review", "In Review"),
        ("completed", "Completed"),
        ("blocked", "Blocked"),
    ]

    id = models.BigAutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=250)
    project = models.IntegerField()
    users = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sprint = models.CharField(max_length=100, null=True, blank=True, default="1")
    release_version = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description  
