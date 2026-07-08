from django.db import models
from .task import Task
from .task_comment import TaskComment
from .organization import Organization


def upload_file_path(instance, filename):
    return f'uploads/user_{instance.user}/{filename}'


class FileUpload(models.Model):
    FILE_TYPES = [
        ('PDF', 'PDF Document'),
        ('DOCX', 'Word Document'),
        ('JPEG', 'JPEG Image'),
        ('PNG', 'PNG Image'),
        ('XLSX', 'Excel Spreadsheet'),
        ('TXT', 'Text File'),
        ('ZIP', 'Compressed Archive'),
    ]

    user = models.IntegerField()
    project = models.IntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    task_comment = models.ForeignKey(TaskComment, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=upload_file_path)
    file_type = models.CharField(max_length=50, choices=FILE_TYPES)
    file_size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"User {self.user} uploaded {self.file.name} on {self.uploaded_at}"
