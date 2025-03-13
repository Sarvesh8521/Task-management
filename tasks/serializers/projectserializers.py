from rest_framework import serializers
from projectserializers import Project

class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.BigAutoField(primary_key=True)
    name = serializers.ForeignObject(max_length=255, unique=True)
    super_user = serializers.ForeignKey(on_delete=serializers.CASCADE)
    sub_user = serializers.ForeignKey( on_delete=serializers.CASCADE, null=True, blank=True, default=None)
    users = serializers.JSONField(default=list) 
    status = serializers.CharField(max_length=20, default="planned",)
    start_date = serializers.DateField(null=True, blank=True)
    end_date = serializers.DateField(null=True, blank=True)
    release_version = serializers.CharField(max_length=100, blank=True)
    sprint = serializers.IntegerField(default=1)
    creation_date = serializers.DateTimeField(auto_now_add=True)
    updation_date = serializers.DateTimeField(auto_now=True)
    is_active = serializers.BooleanField(default=True)



class Meta:
     model = Project
     read_only_feilds = ['start_date', 'end_date', 'release_version',  'creation_date', 'updation_date', 'is_active']
     exclude = ['id','name','status','sprint',]
     fields = ['id', 'name', 'super_user', 'sub_user', 'users', 'status', 'start_date', 'end_date', 'release_version', 'sprint', 'creation_date', 'updation_date', 'is_active']


def validate_Project(self,data):
     return data    