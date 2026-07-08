from rest_framework import serializers
from tasks.models import Task, Project
from user_details.models import User


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    project = serializers.IntegerField()
    users = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES, default="todo")
    issue_type = serializers.ChoiceField(choices=Task.ISSUE_TYPE_CHOICES, default="task")
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES, default="medium")
    start_date = serializers.DateField(allow_null=True, required=False)
    end_date = serializers.DateField(allow_null=True, required=False)
    sprint = serializers.CharField(max_length=100, allow_blank=True, required=False, default="1")
    release_version = serializers.CharField(max_length=100, allow_blank=True, required=False)
    creation_date = serializers.DateTimeField(read_only=True)
    updation_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'project', 'users',
            'status', 'issue_type', 'priority', 'start_date', 'end_date',
            'sprint', 'release_version', 'creation_date', 'updation_date', 'is_active',
        ]
        read_only_fields = ['id', 'creation_date', 'updation_date']

    def validate_project(self, value):
        if not Project.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Project with ID {value} does not exist.")
        return value

    def validate_users(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})
        return data

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance