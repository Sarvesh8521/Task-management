
from django.db import models
from django.utils.timezone import LocalTimezone
from models import User  

class Organization(models.Model):
    id = models.BigAutoField( unique=True, primary_key=True)
    name = models.ForeignKey(max_length=255, unique=True,)
    super_user = models.ForeignKey(User, on_delete=models.CASCADE,)
    sub_user = models.ForeignKey()
    creation_date = models.DateTimeField(LocalTimezone=True)
    updation_date = models.DateTimeField(LocalTimezone=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name