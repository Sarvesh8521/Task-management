from django.db import models
from tasks.models.organization import Organization


class Project(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("on_hold", "On Hold"),
        ("cancelled", "Cancelled"),
    ]

    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    super_user = models.IntegerField()
    sub_user = models.IntegerField()
    user = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    release_version = models.CharField(max_length=100, blank=True)
    sprint = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-creation_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['is_active']),
            models.Index(fields=['super_user']),
        ]

    def __str__(self):
        return self.name
