from rest_framework import serializers
from projectserializers import Project

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
     return data    