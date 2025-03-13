import uuid
from django.db import models
from .user import User
from .refresh_tokens import RefreshToken

class Token(models.Model):
    id = models.BigAutoField(max_length=255, unique=True, editable=False, primary_key=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField(unique=True)
    token_type = models.CharField(max_length=10)
    refresh_token = models.ForeignKey(RefreshToken, on_delete=models.CASCADE)

    def __str__(self):
        return f"Token for {self.user.user_name}"