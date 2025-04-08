
from django.db import models
from django.conf import settings


    


class Profile(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True) 
    app = models.CharField(max_length=255,)
    profile = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return f"Profile of {self.user.user_name}"