from django.db import models
from django.conf import settings
from .task import Task
from .project import Project
from .task_comment import TaskComment
from .organization import Organization

def upload_file_path(instance, filename):
    return f'uploads/{instance.user.username}/{filename}'

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

    Task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)  
    Task_Comment = models.ForeignKey(TaskComment, on_delete=models.CASCADE, null=True, blank=True)  
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)  
    file = models.FileField(upload_to=upload_file_path)  
    file_type = models.CharField(max_length=50, choices=FILE_TYPES)  
    file_size = models.PositiveIntegerField()                     
    uploaded_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user} uploaded {self.file.name} on {self.uploaded_at}"

