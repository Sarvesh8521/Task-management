from django.db import models


class Organization(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    super_user = models.IntegerField(null=False)
    sub_user = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-creation_date']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['super_user']),
        ]

    def __str__(self):
        return self.name
