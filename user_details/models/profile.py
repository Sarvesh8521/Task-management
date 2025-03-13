
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True) 
    app = models.CharField(max_length=255,)
    profile = models.TextField()
    user = models.ForeignKey()
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"Profile of {self.user.user_name}"