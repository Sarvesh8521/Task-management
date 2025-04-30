from rest_framework import serializers
from tasks.models import Project
from enum import Enum
from django.core.exceptions import ValidationError
from user_details.models import User


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    super_user = serializers.IntegerField()
    sub_user = serializers.IntegerField()
    user = serializers.IntegerField()
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
        fields = ['id', 'name', 'super_user', 'sub_user', 'user', 'status','start_date', 'end_date', 'release_version', 'sprint','creation_date', 'updation_date', 'is_active']
    

   
    def create(self, validated_data):
        super_user_id = validated_data.pop('super_user')
        sub_user_id = validated_data.pop('sub_user', None)
        user_id = validated_data.pop('user')

        try:
            super_user = User.objects.get(id=super_user_id)
            user = User.objects.get(id=user_id)
            sub_user = User.objects.get(id=sub_user_id) if sub_user_id else None
        except User.DoesNotExist as e:
            raise serializers.ValidationError(f"User not found: {e}")

        project = Project.objects.create(super_user=super_user.id, sub_user=sub_user.id if sub_user else None, user=user.id, **validated_data)
        return project
    

    # def update(self, instance, validated_data):
    #    if 'project' in validated_data:
    #     instance.project_id = self.validate_project_id(validated_data.pop('project'))

    #    if 'user' in validated_data:
    #     instance.user = self.validate_user(validated_data.pop('user'))

    #    for attr, value in validated_data.items():
    #     setattr(instance, attr, value)

    #    instance.save()
    #    return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def validate_name(self, value):
      if Project.objects.filter(name=value).exists():
        raise ValidationError("Project name is already taken.")
      return value

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
    

    
