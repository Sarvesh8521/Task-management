
from django.db import models
from .roles import Role  

class Scope(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True) 
    name = models.ForeignKey(Role, on_delete=models.CASCADE,max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    updation_date = models.DateTimeField(LocalTimezone=True)

    def __str__(self):
        return f"{self.name} - {self.role.name}"