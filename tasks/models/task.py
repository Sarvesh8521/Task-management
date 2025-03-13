
from django.db import models
from django.utils.timezone import LocalTimezone
from models import User
from .project import Project

class Task(models.Model):
    STATUS_CHOICES = [
        ( 'To Do'),
        ( 'In Progress'),
        ( 'In Review'),
        ( 'Completed'),
        ( 'Blocked'),
    ]

    id = models.BigAutoField( unique=True, primary_key=True)  
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE,)
    users = models.ForeignKey(max_length=255, unique=True, primary_key=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sprint = models.CharField(max_length=100, null=True, blank=True, default=1) 
    release_version = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField(LocalTimezone=True)
    updation_date = models.DateTimeField(LocalTimezone=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    