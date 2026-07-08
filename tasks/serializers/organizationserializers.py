from rest_framework import serializers
from tasks.models import Organization
from user_details.models import User


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    super_user = serializers.IntegerField()
    sub_user = serializers.IntegerField()
    creation_date = serializers.DateTimeField(read_only=True)
    updation_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'super_user', 'sub_user', 'creation_date', 'updation_date', 'is_active']
        read_only_fields = ['id', 'creation_date', 'updation_date']

    def validate(self, data):
        super_user = data.get('super_user')
        sub_user = data.get('sub_user')
        if super_user is not None and sub_user is not None and int(super_user) == int(sub_user):
            raise serializers.ValidationError("Super user and sub user cannot be the same person.")
        return data

    def validate_super_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Super user does not exist.")
        return value

    def validate_sub_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Sub user does not exist.")
        return value

    def create(self, validated_data):
        return Organization.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
