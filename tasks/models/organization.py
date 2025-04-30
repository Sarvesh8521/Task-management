from django.db import models
from django.utils import timezone
from django.conf import settings
from user_details.models import User


class Organization(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    super_user = models.IntegerField(null=False, blank=True)
    sub_user = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
