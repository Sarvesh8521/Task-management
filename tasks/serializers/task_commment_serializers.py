from rest_framework import serializers
from tasks.models import TaskComment, Task, Project
from user_details.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

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
        fields = [
            'id', 'task', 'project', 'user', 'content',
            'created_at', 'updated_at', 'username'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        task_id = validated_data.pop('task')
        project_id = validated_data.pop('project')
        user_id = validated_data.pop('user')

        try:
            task = Task.objects.get(id=task_id)
            project = Project.objects.get(id=project_id)
            user = User.objects.get(id=user_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError("Task not found.")
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project not found.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        comment = TaskComment.objects.create(
            task=task.id,
            project=project.id,
            user=user.id,
            **validated_data
        )
        return comment

    def update(self, instance, validated_data):
        if 'task' in validated_data:
            instance.task = validated_data.pop('task')
        if 'project' in validated_data:
            instance.project = validated_data.pop('project')
        if 'user' in validated_data:
            instance.user = validated_data.pop('user')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate_content(self, value):
        if not value.strip():
            raise ValidationError("Comment content cannot be empty.")
        return value

    def validate(self, data):
        created_at = data.get('created_at')
        updated_at = data.get('updated_at')

        if created_at and created_at > datetime.now():
            raise serializers.ValidationError("Created date cannot be in the future.")

        if updated_at and updated_at > datetime.now():
            raise serializers.ValidationError("Updated date cannot be in the future.")

        return data
