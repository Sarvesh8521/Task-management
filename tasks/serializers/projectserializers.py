from rest_framework import serializers
from tasks.models import Project
from user_details.models import User


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    super_user = serializers.IntegerField()
    sub_user = serializers.IntegerField()
    user = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Project.STATUS_CHOICES, default="planned")
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    release_version = serializers.CharField(max_length=100, required=False, allow_blank=True)
    sprint = serializers.IntegerField(required=False, default=1)
    creation_date = serializers.DateTimeField(read_only=True)
    updation_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'super_user', 'sub_user', 'user',
            'status', 'start_date', 'end_date', 'release_version', 'sprint',
            'creation_date', 'updation_date', 'is_active',
        ]
        read_only_fields = ['id', 'creation_date', 'updation_date']

    def validate_name(self, value):
        """Allow same name on update, reject duplicates on create."""
        queryset = Project.objects.filter(name=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Project name is already taken.")
        return value

    def validate_super_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Super user does not exist.")
        sub_user = self.initial_data.get('sub_user')
        if sub_user is not None and int(value) == int(sub_user):
            raise serializers.ValidationError("Super user and sub user cannot be the same.")
        return value

    def validate_sub_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Sub user does not exist.")
        return value

    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})
        return data

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
