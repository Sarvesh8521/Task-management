from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.BigAutoField(primary_key=True)  
    description = serializers.TextField(max_length=500)
    project = serializers.ForeignKey(on_delete=serializers.CASCADE,)
    users = serializers.ForeignKey(max_length=255, unique=True, primary_key=True) 
    status = serializers.CharField(max_length=20, default="todo")
    start_date = serializers.DateField(null=True, blank=True)
    end_date = serializers.DateField(null=True, blank=True)
    sprint = serializers.CharField(max_length=100, null=True, blank=True, default=1) 
    release_version = serializers.CharField(max_length=100, blank=True)
    creation_date = serializers.DateTimeField(LocalTimezone=True)
    updation_date = serializers.DateTimeField(LocalTimezone=True)
    is_active = serializers.BooleanField(default=True)




class Meta:
    model = Task
    read_only_feilds = ['creation_date', 'updation_date', 'is_active','creation_date', 'updation_date',]
    exclude = ['id','description','sprint','release_version',]
    fields = ['id', 'description', 'project', 'users', 'status', 'start_date', 'end_date', 'sprint', 'release_version',  'creation_date', 'updation_date', 'is_active']



def validate_project(self, value):
        if not Task(id=value.id).exists():
            raise ValidationError(f"Project with ID {value.id} does not exist.")
        return value



def validate_users_active(self, value):
  for user in value:
            if not user.is_active:
                raise ValidationError(f"User {user.username} is not active.")
            return value
  
def validate_user(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value

  




def validate_status(self, value):
        allowed_statuses = ["todo", "in-progress", "completed"]
        if value not in allowed_statuses:
            raise ValidationError(f"Invalid Allowed statuses are: {', '.join(allowed_statuses)}.")
        return value





def validate_dates(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
        return data
    


    
def task_create(self, validated_data):
        return Task(validated_data)