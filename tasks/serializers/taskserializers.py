from rest_framework import serializers
from tasks.models import Task,Project
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from user_details.models import User
from tasks.models import project




class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)
    project = serializers.IntegerField()  
    users = serializers.IntegerField( )
    # user = serializers.IntegerField(source= 'user_id')
    status = serializers.ChoiceField(["todo", "in-progress", "completed"], default="todo")
    start_date = serializers.DateField(allow_null=True, required=False)
    end_date = serializers.DateField(allow_null=True, required=False)
    sprint = serializers.CharField(max_length=100, allow_blank=True, required=False, default="1") 
    release_version = serializers.CharField(max_length=100, allow_blank=True, required=False)
    creation_date = serializers.DateTimeField(default=now, read_only=True)
    updation_date = serializers.DateTimeField(default=now, read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Task
        read_only_fields = ['creation_date', 'updation_date', 'is_active']
        fields = ['id', 'name','description', 'project', 'users', 'status', 'start_date', 'end_date', 'sprint', 'release_version', 'creation_date', 'updation_date', 'is_active']

    def validate_project(self, value):
        if not Project.objects.filter(id=value).exists():
            raise ValidationError(f"Project with ID {value} not exist.")
        return value
    
    # def validate_project(self, value):
    #     try:
    #         Project.objects.get(id=value)
    #     except Project.DoesNotExist:
    #         raise ValidationError(f"Project with ID {value} does not exist.")
    #     return value

    def validate_users(self, value):
        if not User.objects.filter(id=value).exists():
            raise ValidationError("User does not exist.")
        return value


    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def validate_status(self, value):
        allowed_statuses = ["todo", "in-progress", "completed"]
        if value not in allowed_statuses:
            raise ValidationError(f"Invalid status. Allowed statuses are: {', '.join(allowed_statuses)}.")
        return value

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
        return data


    # def create(self, validated_data):
    #     users = validated_data.pop('users')
    #     project = validated_data.pop('project')
    #     task = Task.objects.create(project=project, **validated_data)
    #     task.users.set(users)
    #     return task
    
    # def create(self, validated_data):
    #     user_id = validated_data.pop('users')
    #     # project_id = validated_data.pop('project')
        
        
    #     # project = Project.objects.get(id=project_id)
    #     # user = User.objects.get(id=user_id)
    #     task = Task.objects.create(project=project, **validated_data)
    #     task.users.add(user_id)  # For ManyToMany, use .set([user]) if multiple users
    #     return task


    # def update(self, instance, validated_data):
    #     if 'project' in validated_data:
    #         instance.project = self.validate_project(validated_data.pop('project'))
    #     if 'user' in validated_data:
    #         instance.user = self.validate_user(validated_data.pop('user'))

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance
    
    # def update(self, instance, validated_data):
    #     if 'project' in validated_data:
    #         project_id = validated_data.pop('project')
    #         instance.project = Project.objects.get(id=project_id)
        
    #     if 'users' in validated_data:
    #         user_id = validated_data.pop('users')
    #         # instance.users.clear()  # Clear existing if ManyToMany
    #         instance.users.add(User.objects.get(id=user_id))

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance



# def validate_dates(self, data):
#         start_date = data.get('start_date')
#         end_date = data.get('end_date')
#         if start_date and end_date and start_date > end_date:
#             raise ValidationError("Start date cannot be after end date.")
#         return data