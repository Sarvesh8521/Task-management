from rest_framework import serializers
from projectserializers import Project
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.BigAutoField(primary_key=True)
    name = serializers.CharField(max_length=255, unique=True)
    super_user = serializers.CharField(max_length=255, unique=True,)
    sub_user = serializers.CharField(max_length=255, unique=True,)
    users = serializers.foreignkey(max_length=255, unique=True,) 
    status = serializers.CharField(max_length=20, default="planned",)
    start_date = serializers.DateField(null=True, blank=True)
    end_date = serializers.DateField(null=True, blank=True)
    release_version = serializers.CharField(max_length=100, blank=True)
    sprint = serializers.CharField(max_length=100, null=True, blank=True, default=1) 
    creation_date = serializers.DateTimeField(auto_now_add=True)
    updation_date = serializers.DateTimeField(auto_now=True)
    is_active = serializers.BooleanField(default=True)



class Meta:
     model = Project
     read_only_feilds = ['start_date', 'end_date', 'release_version',  'creation_date', 'updation_date', 'is_active']
     exclude = ['id','name','status','sprint',]
     fields = ['id', 'name', 'super_user', 'sub_user', 'users', 'status', 'start_date', 'end_date', 'release_version', 'sprint', 'creation_date', 'updation_date', 'is_active']


def validate_project(self,data):
     if Project(name=data).exists():
            raise ValidationError(" name is already taken")
     return data    



def validate_super_user(self, value):
        if value == self.initial_data.get('sub_user'):
            raise ValidationError(" super user and sub user cannot be the same.")
        return value

def validate_sub_user(self, value):
        if value == self.initial_data.get('super_user'):
            raise ValidationError(" sub user and super user cannot be the same.")
        return value

def validate_users(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value



def validate_status(self, value):
        
        valid_statuses = ["planned", "in-progress", "completed"]
        if value not in valid_statuses:
            raise ValidationError(f"Invalid. Allowed values {', '.join(valid_statuses)}.")
        return value



def validate_date(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Start date cannot be after end date.")
        return data