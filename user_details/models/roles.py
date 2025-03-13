
from django.db import models

class Role(models.models):
    id = models.BigAutoField(max_length=255, unique=True, primary_key=True, editable=False) 
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=True)
    updation_date = models.DateTimeField(default=True)

    def __str__(self):
        return self.name