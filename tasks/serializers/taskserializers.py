
from rest_framework import serializers
from tasks.models import Task
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from user_details.models import User




class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(max_length=500)
    project = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())  
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    status = serializers.ChoiceField(choices=["todo", "in-progress", "completed"], default="todo")
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
        exclude = ['id', 'sprint', 'release_version']
        fields = [
            'id', 'description', 'project', 'users', 'status', 
            'start_date', 'end_date', 'sprint', 'release_version', 
            'creation_date', 'updation_date', 'is_active'
        ]

    def validate_project(self, value):
        """Ensure the project exists before assigning it."""
        if not Task.objects.filter(id=value.id).exists():
            raise ValidationError(f"Project with ID {value.id} does not exist.")
        return value

    def validate_users(self, value):
        """Ensure users are active before assigning them to a task."""
        inactive_users = [user.username for user in value if not user.is_active]
        if inactive_users:
            raise ValidationError(f"The following users are not active: {', '.join(inactive_users)}.")
        return value

    def validate_status(self, value):
        """Validate that status is allowed."""
        allowed_statuses = ["todo", "in-progress", "completed"]
        if value not in allowed_statuses:
            raise ValidationError(f"Invalid status. Allowed statuses are: {', '.join(allowed_statuses)}.")
        return value

    def validate(self, data):
        """Ensure start_date is before end_date."""
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
        return data

    def create(self, validated_data):
        """Create a new task with validated data."""
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update task and set updation_date automatically."""
        instance.updation_date = now()
        return super().update(instance, validated_data)
    

# def validate_users_active(self, value):
#   for user in value:
#             if not user.is_active:
#                 raise ValidationError(f"User {user.username} is not active.")
#             return value
  
# def validate_user(self, value):
#         if not User.exists():
#             raise ValidationError(f"User does not exist.")
#         return value

  





def validate_dates(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
        return data
    
