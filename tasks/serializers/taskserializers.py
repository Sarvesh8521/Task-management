from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.BigAutoField(primary_key=True)  
    description = serializers.TextField()
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

    def create(self, validated_data):
        return Task.objects.create(**validated_data)