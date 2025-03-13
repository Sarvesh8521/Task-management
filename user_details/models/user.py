
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import LocalTimezone

class User(User):
    id = models.BigAutoField(unique=True, primary_key=True)
    user_id = models.BigAutoField(primary_key=True, editable=False, unique=True)
    user_name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True,max_length=124)
    password = models.CharField(max_length=100)  
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(LocalTimezone=True)
    updation_date = models.DateTimeField(LocalTimezone=True)




    def __str__(self):
        return self.user_name