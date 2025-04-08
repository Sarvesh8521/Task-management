from django.db import models
from tasks.models.organization import Organization
from django.conf import settings



class Project(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("on_hold", "On Hold"),
        ("cancelled", "Cancelled"),
    ]

    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=255, unique=True)  
    super_user = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="supervised_projects")
    sub_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="sub_projects")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    release_version = models.CharField(max_length=100, blank=True)
    sprint = models.IntegerField(default=1)  
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
