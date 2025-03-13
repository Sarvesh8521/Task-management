
from django.db import models
from .user import User
from .roles import Role
from django.utils.timezone import LocalTimezone

class UserRole(models.Model):
    id = models.BigAutoField(max_length=255, unique=True, primary_key=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scope = models.ForeignKey()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    updation_date = models.DateTimeField(LocalTimezone=True)

    def __str__(self):
        return f"{self.user.user_name} - {self.role.name}"