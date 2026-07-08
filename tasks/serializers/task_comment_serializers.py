from rest_framework import serializers
from tasks.models import TaskComment, Task, Project
from user_details.models import User


class TaskCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    task = serializers.IntegerField()
    project = serializers.IntegerField()
    user = serializers.IntegerField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'project', 'user', 'content', 'created_at', 'updated_at', 'username']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value

    def validate_task(self, value):
        if not Task.objects.filter(id=value).exists():
            raise serializers.ValidationError("Task not found.")
        return value

    def validate_project(self, value):
        if not Project.objects.filter(id=value).exists():
            raise serializers.ValidationError("Project not found.")
        return value

    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found.")
        return value

    def create(self, validated_data):
        return TaskComment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
