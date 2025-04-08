from django.db import models
from django.utils import timezone
from django.conf import settings


class Organization(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    super_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="super_organizations" )
    sub_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_organizations")
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
