
from django.db import models
from django.utils.timezone import LocalTimezone
from datetime import timedelta

class RefreshToken(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True, editable=False) 
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    refresh_token = models.TextField(unique=True)
    is_active = models.BooleanField(default=True)
    counter = models.IntegerField(default=0)
    token = models.ForeignKey(on_delete=models.CASCADE)
    expires_at = models.DateTimeField(LocalTimezone=True)
    creation_date = models.DateTimeField(LocalTimezone=True)
    updation_date = models.DateTimeField(LocalTimezone=True)

    def __str__(self):
        return f" RefreshToken for {self.user.user_name} (Expires: {self.expires_at})"