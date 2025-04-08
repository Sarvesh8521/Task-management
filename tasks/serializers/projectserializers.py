from rest_framework import serializers
from tasks.models import Project
from django.core.exceptions import ValidationError
from user_details.models import User


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField(max_length=255)
    super_user = serializers.CharField(max_length=255)
    sub_user = serializers.CharField(max_length=255)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    status = serializers.CharField(max_length=20, default="planned")
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    release_version = serializers.CharField(max_length=100, required=False, allow_blank=True)
    sprint = serializers.CharField(max_length=100, required=False, allow_blank=True)
    creation_date = serializers.DateTimeField(read_only=True)
    updation_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Project
        read_only_fields = ['start_date', 'end_date', 'release_version', 'creation_date', 'updation_date', 'is_active']
        fields = [
            'id', 'name', 'super_user', 'sub_user', 'users', 'status',
            'start_date', 'end_date', 'release_version', 'sprint',
            'creation_date', 'updation_date', 'is_active'
        ]

    def validate_project(self, data):
        if Project.objects.filter(name=data).exists():
            raise ValidationError("Name is already taken")
        return data    

    def validate_super_user(self, value):
        if value == self.initial_data.get('sub_user'):
            raise ValidationError("Super user and sub user cannot be the same.")
        return value

    def validate_sub_user(self, value):
        if value == self.initial_data.get('super_user'):
            raise ValidationError("Sub user and super user cannot be the same.")
        return value

    def validate_users(self, value):
        if not User.objects.exists():
            raise ValidationError("User does not exist.")
        return value

    def validate_status(self, value):
        valid_statuses = ["planned", "in-progress", "completed"]
        if value not in valid_statuses:
            raise ValidationError(f"Invalid. Allowed values: {', '.join(valid_statuses)}.")
        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
        return data
