
from django.db import models
from django.utils.timezone import now
import uuid


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True, max_length=124)
    password = models.CharField(max_length=100)  
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=now)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
