from rest_framework import serializers
from ..models import Organization
from django.core.exceptions import ValidationError
from user_details.models import User





class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    name = serializers.CharField(max_length=255)
    super_user = serializers.CharField(max_length=255)
    sub_user = serializers.CharField(max_length=255)
    creation_date = serializers.DateTimeField(read_only=True)
    updation_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)
    sprint = serializers.CharField(max_length=100, required=False, allow_blank=True, default='1')

    class Meta:
        model = Organization
        read_only_fields = ['creation_date', 'updation_date', 'is_active']
        fields = ['id', 'name', 'super_user', 'sub_user', 'creation_date', 'updation_date', 'is_active', 'sprint']


    def validate(self, data):
        if data.get('super_user') == data.get('sub_user'):
            raise ValidationError("you've assigned the same person as both")
        return data

    def validate_super_user(self, value):
        if value == self.initial_data.get('sub_user'):
            raise ValidationError("Please choose a different sub user.")
        return value

    def validate_sub_user(self, value):
        if value == self.initial_data.get('super_user'):
            raise ValidationError(" Please choose a different super user.")
        return value

    def validate_user(self, value):
        if not User.objects.filter(pk=value.pk).exists():
            raise ValidationError("User does not exist.")
        return value
