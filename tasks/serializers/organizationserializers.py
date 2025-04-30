from rest_framework import serializers
from tasks.models import Organization
from django.core.exceptions import ValidationError
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
        read_only_fields = ['creation_date', 'updation_date', 'is_active']
        fields = ['id', 'name', 'super_user', 'sub_user', 'creation_date', 'updation_date', 'is_active', ]


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



    def create(self, validated_data):
        super_user_id = validated_data.pop('super_user')  
        sub_user_id = validated_data.pop('sub_user')  

        organization = Organization.objects.create(
            super_user=super_user_id,
            sub_user=sub_user_id,
            **validated_data
        )
        return organization
    

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
