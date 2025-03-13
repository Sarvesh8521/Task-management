
from django.db import models
from django.utils.timezone import now
from models import User
from models.organization import Organization

class Project(models.Model):
    STATUS_CHOICES = [
        ( 'Planned'),
        ( 'In Progress'),
        ( 'Completed'),
        ( 'On Hold'),
        ( 'Cancelled'),
    ]

    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    name = models.ForeignObject(max_length=255, unique=True)
    super_user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None) #models.JSONField( blank=True,)
    users = models.JSONField(default=list) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned",)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    release_version = models.CharField(max_length=100, blank=True)
    sprint = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name